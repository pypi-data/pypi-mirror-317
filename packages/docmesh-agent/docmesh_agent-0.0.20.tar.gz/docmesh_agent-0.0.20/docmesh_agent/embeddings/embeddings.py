from langchain_openai import OpenAIEmbeddings

from docmesh_core.db.neo.paper import list_unembedded_papers, update_papers

EMBEDDING_MODEL = "text-embedding-3-large"
NUM_DIMENSIONS = 1024


def query_embeddings(query: str) -> list[float]:
    # setup embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=NUM_DIMENSIONS)
    query_embedded = embeddings.embed_query(query)

    return query_embedded


def update_paper_embeddings(n: int) -> int:
    unembedded_papers = list_unembedded_papers(n=n)

    if unembedded_papers.shape[0] == 0:
        return 0

    # setup embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=NUM_DIMENSIONS)

    texts = unembedded_papers.apply(
        lambda x: f"{x.title}\n{x.abstract}\n{x.summary}",
        axis=1,
    )
    texts_embedded = embeddings.embed_documents(texts.to_list())
    unembedded_papers["embedding_te3l"] = texts_embedded

    update_papers(unembedded_papers)
    update_cnt = unembedded_papers.shape[0]

    return update_cnt
