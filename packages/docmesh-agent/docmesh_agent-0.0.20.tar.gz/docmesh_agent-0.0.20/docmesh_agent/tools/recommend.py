from typing import Type, Optional
from pydantic import BaseModel, Field

from datetime import datetime
from langchain.callbacks.manager import CallbackManagerForToolRun


from docmesh_core.db.neo.recommend import (
    recommend_follows_papers,
    recommend_influential_papers,
    recommend_similar_papers,
    recommend_semantic_papers,
)
from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.embeddings.embeddings import query_embeddings


class UnreadFollowsToolInput(BaseModel):
    n: int = Field(description="number of papers")


class UnreadFollowsTool(BaseAgentTool):
    name: str = "recommend_papers_from_follows"
    description: str = "useful when you need to get some recommanded papers from follows"
    args_schema: Optional[Type[BaseModel]] = UnreadFollowsToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        df = recommend_follows_papers(entity_name=self.entity_name, n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadInfluentialToolInput(BaseModel):
    date_time: str = Field(description="publication date time of papers")
    n: int = Field(description="number of papers")


class UnreadInfluentialTool(BaseAgentTool):
    name: str = "recommend_latest_influential_papers"
    description: str = "useful when you need to get some influential papers from a given date"
    args_schema: Optional[Type[BaseModel]] = UnreadInfluentialToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        date_time: str,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        date_time = self._preporcess_input(date_time)
        try:
            datetime.strptime(date_time, "%Y-%m-%d")
        except Exception:
            self._raise_tool_error(
                "Input argument `date_time` should be written in format `YYYY-MM-DD`, "
                "please check your input, valid input can be 1995-03-01, 2024-01-01.\n"
            )

        df = recommend_influential_papers(
            entity_name=self.entity_name,
            date_time=date_time,
            n=n,
        )
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadSimilarToolInput(BaseModel):
    paper_id: str = Field(description="paper id")
    n: int = Field(description="number of papers")


class UnreadSimilarTool(BaseAgentTool):
    name: str = "recommend_similar_papers"
    description: str = "useful when you need to get some similar papers from provided paper id"
    args_schema: Optional[Type[BaseModel]] = UnreadSimilarToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        df = recommend_similar_papers(
            entity_name=self.entity_name,
            paper_id=paper_id,
            n=n,
        )
        # keep score over 0.5 and drop the column
        df = df[df["score"] > 0.5].drop(columns="score")
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadSemanticToolInput(BaseModel):
    query: str = Field(description="search query")
    n: int = Field(description="number of papers")


class UnreadSemanticTool(BaseAgentTool):
    name: str = "recommend_queried_papers"
    description: str = "useful when you need to get some papers from a query"
    args_schema: Optional[Type[BaseModel]] = UnreadSemanticToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        query: str,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        query = self._preporcess_input(query)
        query_embedded = query_embeddings(query)

        df = recommend_semantic_papers(
            entity_name=self.entity_name,
            semantic_embedding=query_embedded,
            n=n,
        )
        # keep score over 0.5 and drop the column
        df = df[df["score"] > 0.5].drop(columns="score")
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
