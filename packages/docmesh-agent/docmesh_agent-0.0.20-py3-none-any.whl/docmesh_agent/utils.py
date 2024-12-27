import os
import re

from typing import Any
from pydantic import BaseModel, Field

from qcloud_cos import CosConfig, CosS3Client
from sqlalchemy import create_engine

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts.image import ImagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from docmesh_core.db.neo.paper import get_paper, PDFNotFound
from docmesh_core.db.figure import get_figures, add_figures
from docmesh_core.db.poster import get_poster, add_poster
from docmesh_core.cos import get_cos_figures, upload_cos_figures
from docmesh_core.utils.figure_extraction import extract_figures
from docmesh_agent.loader import ImagePDFProxyLoader, PyMuPDFProxyLoader

# setup mysql engine
if (mysql_url := os.getenv("MYSQL_URL")) is None:
    raise ValueError("You have to set mysql database url using environment `MYSQL_URL`.")
else:
    engine = create_engine(mysql_url, pool_pre_ping=True, pool_recycle=3600)

# setup cos client
secret_id = os.getenv("COS_SECRET_ID")
secret_key = os.getenv("COS_SECRET_KEY")
region = os.getenv("COS_REGION")
bucket = os.getenv("COS_BUCKET")
domain = os.getenv("COS_DOMAIN")
token = None
scheme = "https"

config = CosConfig(
    Region=region,
    SecretId=secret_id,
    SecretKey=secret_key,
    Token=token,
    Scheme=scheme,
    Domain=domain,
)
client = CosS3Client(config)


class Poster(BaseModel):
    title: str = Field(description="title of the paper")
    authors: str = Field(description="authors of the paper")
    background: str = Field(description="background of the paper")
    method: str = Field(description="detailed method of the paper")
    experiment: str = Field(description="detailed experiment of the paper")
    result: str = Field(description="detailed result of the paper")
    conclusion: str = Field(description="conclusion of the paper")


def extract_figures_from_paper(paper_id: str) -> list[str]:
    paper = get_paper(paper=paper_id)

    if not (figures := get_figures(engine=engine, paper_id=paper_id)):
        if not paper.pdf:
            raise PDFNotFound(paper_id)

        figures = extract_figures_from_pdf(pdf=paper.pdf)
        add_figures(engine=engine, paper_id=paper_id, figures=figures)

    figures_urls = get_cos_figures(client=client, bucket=bucket, figures=figures)

    return figures_urls


def extract_figures_from_pdf(pdf: str) -> list[str]:
    loader = ImagePDFProxyLoader(pdf)
    images = loader.load()

    figures = []
    for image in images:
        figures.extend(extract_figures(image))

    figure_names = upload_cos_figures(client=client, bucket=bucket, figures=figures)

    return figure_names


def replace_images_in_markdown(markdown, images):
    # Pattern to match markdown image placeholders
    pattern = r"!\[(.*?)\]\((\d+)\)"

    def replacer(match):
        # Extract the image index from the markdown
        img_index = int(match.group(2))
        # Replace with the actual image path or data
        if 0 <= img_index < len(images):
            return f"![{match.group(1)}]({images[img_index]})"
        return match.group(0)  # Keep original if index is invalid

    # Replace all matches in the markdown
    return re.sub(pattern, replacer, markdown)


def replace_images_in_poster(
    poster: dict[str, Any],
    figures_urls: list[str],
) -> dict[str, Any]:

    poster["method"] = replace_images_in_markdown(poster["method"], figures_urls)
    poster["experiment"] = replace_images_in_markdown(poster["experiment"], figures_urls)
    poster["result"] = replace_images_in_markdown(poster["result"], figures_urls)

    return poster


def get_poster_from_db(poster_id: str) -> dict[str, Any]:
    poster = get_poster(engine=engine, poster_id=poster_id)
    paper_id = poster["paper_id"]

    # get figures urls
    figures = get_figures(engine=engine, paper_id=paper_id)
    figures_urls = get_cos_figures(client=client, bucket=bucket, figures=figures if figures else [])

    # replace images in poster
    poster = replace_images_in_poster(poster=poster, figures_urls=figures_urls)

    return poster


def generate_poster_from_paper(paper_id: str, entity_name: str, model: str) -> dict[str, str]:
    paper = get_paper(paper=paper_id)
    if not paper.pdf:
        raise PDFNotFound(paper_id)

    # get figures urls
    figures = get_figures(engine=engine, paper_id=paper_id)
    figures_urls = get_cos_figures(client=client, bucket=bucket, figures=figures if figures else [])

    # generate poster from pdf
    poster = generate_poster_from_pdf(pdf=paper.pdf, model=model, figures_urls=figures_urls)
    # update poster to db
    poster_id = add_poster(
        engine=engine,
        paper_id=paper_id,
        entity_name=entity_name,
        pdf=paper.pdf,
        # title should alwarys follow the original paper title
        title=paper.title,
        authors=poster.authors,
        background=poster.background,
        method=poster.method,
        experiment=poster.experiment,
        result=poster.result,
        conclusion=poster.conclusion,
    )

    # dump base model to dictionary
    poster = poster.model_dump()
    # post process poster - replace images in markdown
    poster = replace_images_in_poster(poster=poster, figures_urls=figures_urls)
    # add poster id and pdf to data
    poster["poster_id"] = poster_id
    poster["pdf"] = paper.pdf
    poster["title"] = paper.title
    return poster


def generate_poster_from_pdf(pdf: str, model: str, figures_urls: list[str] = []) -> Poster:
    # setup llm
    llm = ChatOpenAI(model=model)

    # phrase 1 - text based poster
    loader = PyMuPDFProxyLoader(pdf)
    pages = loader.load()
    paper_content = "\n".join([page.page_content for page in pages])
    # load text based poster prompt
    prompt = hub.pull(os.getenv("DOCMESH_AGENT_PAPER_POST_PROMPT"))
    parser = PydanticOutputParser(pydantic_object=Poster)
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser
    # generate text based poster
    text_poster: Poster = chain.invoke({"paper_content": paper_content})

    # phrase 2 - image based poster
    if figures_urls:
        figures_prompts = [
            HumanMessagePromptTemplate(
                prompt=[
                    ImagePromptTemplate(
                        input_variables=["image_url"],
                        template={"url": "{image_url}"},
                    ),
                ],
            ).format(image_url=figure_url)
            for figure_url in figures_urls
        ]
        # load image based poster prompt
        prompt = hub.pull(os.getenv("DOCMESH_AGENT_PAPER_POST_FIGURES_PROMPT"))
        prompt = prompt.partial(
            figures=figures_prompts,
            format_instructions=parser.get_format_instructions(),
        )
        chain = prompt | llm | parser
        # generate image based poster
        image_poster: Poster = chain.invoke({"paper_poster": text_poster.model_dump()})
        poster = image_poster
    else:
        poster = text_poster

    return poster
