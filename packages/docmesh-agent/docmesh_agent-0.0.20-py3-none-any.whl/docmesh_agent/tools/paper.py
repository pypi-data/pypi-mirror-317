import os

from typing import Type, Optional
from pydantic import BaseModel, Field

from langchain import hub
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts.image import ImagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

from docmesh_core.db.neo.paper import get_paper, add_paper
from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_agent.loader import PyMuPDFProxyLoader
from docmesh_agent.utils import extract_figures_from_paper
from docmesh_agent.tools.base import BaseAgentTool, BaseAgentLLMTool


class AddPaperToolInput(BaseModel):
    paper: str = Field(description="paper title or arxiv id")


class AddPaperTool(BaseAgentTool):
    name: str = "add_paper"
    description: str = "useful when you need to add a paper using title or arxiv id"
    args_schema: Optional[Type[BaseModel]] = AddPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper = self._preporcess_input(paper)
        paper_id = get_paper_id(paper=paper)

        if paper_id is None:
            self._raise_tool_error(f"Cannot find paper id for {paper}, you may end execution.")

        try:
            add_paper(paper_id=paper_id)
            msg = f"Successfully add paper {paper} with id {paper_id} into database."
        except Exception as e:
            msg = f"Failed to add paper {paper} into database with error: {e}."

        return f"\n{msg}\n"


class GetPaperIdToolInput(BaseModel):
    paper: str = Field(description="paper title")


class GetPaperIdTool(BaseAgentTool):
    name: str = "get_paper_id"
    description: str = "useful when you need to find a paper id"
    args_schema: Optional[Type[BaseModel]] = GetPaperIdToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper = self._preporcess_input(paper)
        paper_id = get_paper_id(paper=paper)

        if paper_id is None:
            self._raise_tool_error(f"Cannot find paper id for {paper}, you may end execution.")

        try:
            paper_id = get_paper(paper=paper_id).paper_id
            msg = f"Successfully find paper id {paper_id} for {paper}."
        except Exception as e:
            msg = f"Failed to find paper id for {paper} with error: {e}."

        return f"\n{msg}\n"


class GetPaperDetailsToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class GetPaperDetailsTool(BaseAgentTool):
    name: str = "get_paper_details"
    description: str = (
        "useful when you need to get details of a paper, "
        "including citation count, reference cound, publication date and pdf link if available"
    )
    args_schema: Optional[Type[BaseModel]] = GetPaperDetailsToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)

        try:
            paper = get_paper(paper=paper_id)
        except Exception:
            self._raise_tool_error(
                "Input argument `paper_id` should be a valid paper id, please check your input. "
                "Pay attention that the paper id is not arxiv id."
            )

        paper_details = paper.serialize
        msg = "\n".join(f"{k}: {v}" for k, v in paper_details.items())
        return f"\n{msg}\n"


class GetPaperPDFToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class GetPaperPDFTool(BaseAgentTool):
    name: str = "get_paper_pdf_link"
    description: str = "useful when you need to find the pdf of a paper"
    args_schema: Optional[Type[BaseModel]] = GetPaperPDFToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)

        try:
            paper = get_paper(paper=paper_id)
        except Exception:
            self._raise_tool_error(
                "Input argument `paper_id` should be a valid paper id, please check your input. "
                "Pay attention that the paper id is not arxiv id."
            )

        if paper.pdf is None:
            msg = "Unable to find the pdf link for provided paper."
        else:
            msg = paper.pdf

        return f"\n{msg}\n"


class ReadWholePDFToolInput(BaseModel):
    pdf_link: str = Field(description="pdf link of paper")


class ReadWholePDFTool(BaseAgentTool):
    name: str = "read_whole_pdf"
    description: str = "useful when you need to read the whole PDF content, use if with cautions"
    args_schema: Optional[Type[BaseModel]] = ReadWholePDFToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        pdf_link: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        pdf_link = self._preporcess_input(pdf_link)

        try:
            loader = PyMuPDFProxyLoader(pdf_link)
            pages = loader.load()
            msg = "\n".join([page.page_content for page in pages])
        except Exception:
            msg = "Failed to read the PDF content."

        return f"\n{msg}\n"


class ReadPartialPDFToolInput(BaseModel):
    pdf_link: str = Field(description="pdf link of paper")
    query: str = Field(description="search query")


class ReadPartialPDFTool(BaseAgentTool):
    name: str = "read_partial_pdf"
    description: str = "useful when you need to read partial PDF content with query"
    args_schema: Optional[Type[BaseModel]] = ReadPartialPDFToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        pdf_link: str,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        pdf_link = self._preporcess_input(pdf_link)

        try:
            loader = PyMuPDFProxyLoader(pdf_link)
            pages = loader.load()

            faiss_index = FAISS.from_documents(
                pages,
                OpenAIEmbeddings(
                    base_url=os.getenv("OPENAI_EMBEDDING_API_BASE"),
                    api_key=os.getenv("OPENAI_EMBEDDING_API_KEY"),
                    model=os.getenv("OPENAI_EMBEDDING_MODEL"),
                ),
            )
            similar_pages = faiss_index.similarity_search(query, k=2)
            msg = "\n".join([f"Paragraph: {i + 1}\n{page.page_content}" for i, page in enumerate(similar_pages)])
        except Exception:
            msg = "Failed to read the PDF content."
        return f"\n{msg}\n"


class ExtractFiguresToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class ExtractFiguresTool(BaseAgentTool):
    name: str = "extract_figures"
    description: str = "useful when you need to extract figures from a paper"
    args_schema: Optional[Type[BaseModel]] = ExtractFiguresToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)

        try:
            figures = extract_figures_from_paper(paper_id=paper_id)
            msg = "\n".join([f"![Figure {i + 1}]({figure})" for i, figure in enumerate(figures)])
        except Exception as e:
            msg = f"Failed to extract figures from the PDF with error: {e}."

        return f"\n{msg}\n"


class PaperPosterToolInput(BaseModel):
    pdf_link: str = Field(description="pdf link of paper")
    figures_urls: list[str] = Field(description="list of figure urls")


class PaperPosterTool(BaseAgentLLMTool):
    name: str = "paper_poster"
    description: str = "useful when you need to genearte the paper poster"
    args_schema: Optional[Type[BaseModel]] = PaperPosterToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        pdf_link: str,
        figures_urls: list[str],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        pdf_link = self._preporcess_input(pdf_link)

        try:
            loader = PyMuPDFProxyLoader(pdf_link)
            pages = loader.load()
            paper_content = "\n".join([page.page_content for page in pages])

            # construct multi-modal input
            figures = [
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
            # load summary prompt
            prompt = hub.pull(os.getenv("DOCMESH_AGENT_PAPER_SUMMARY_PROMPT"))
            prompt = prompt.partial(figures=figures)
            chain = prompt | self.llm | StrOutputParser()

            res = chain.invoke({"paper_content": paper_content})
            msg = f"poster content: {res}, please ensure use the figure link to generate the poster."
        except Exception as e:
            self._raise_tool_error(f"Failed to generate paper poster with error: {e}.")

        return f"\n{msg}\n"
