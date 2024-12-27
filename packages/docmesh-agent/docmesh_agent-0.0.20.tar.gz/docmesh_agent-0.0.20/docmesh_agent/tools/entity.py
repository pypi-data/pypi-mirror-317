from datetime import datetime

from typing import Type, Optional
from pydantic import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun

from docmesh_core.db.neo.entity import (
    list_follows,
    list_followers,
    list_popular_entities,
    follow_entity,
    subscribe_venue,
    list_subscriptions,
    mark_paper_read,
    save_paper_list,
    list_reading_list,
    list_latest_reading_papers,
    list_recent_reading_papers,
)
from docmesh_agent.tools.base import BaseAgentTool, BaseAgentNoInputTool


class ListFollowsTool(BaseAgentNoInputTool):
    name: str = "list_follows"
    description: str = "useful when you need to list all your follows"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        df = list_follows(entity_name=self.entity_name)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class ListFollowersTool(BaseAgentNoInputTool):
    name: str = "list_followers"
    description: str = "useful when you need to list all your followers"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        df = list_followers(entity_name=self.entity_name)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class ListPopularEntitiesToolInput(BaseModel):
    n: int = Field(description="number of entities")


class ListPopularEntitiesTool(BaseAgentTool):
    name: str = "list_popular_entities"
    description: str = "useful when you need to list popular entities"
    args_schema: Optional[Type[BaseModel]] = ListPopularEntitiesToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        df = list_popular_entities(n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class FollowEntityToolInput(BaseModel):
    name: str = Field(description="entity name")


class FollowEntityTool(BaseAgentTool):
    name: str = "follow_entity"
    description: str = "uesful when you need to follow an entity"
    args_schema: Optional[Type[BaseModel]] = FollowEntityToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        name = self._preporcess_input(name)
        follow_entity(self.entity_name, name)
        return f"\nSuccessfully follow entity {name}\n"


class SubscribeVenueToolInput(BaseModel):
    venue_name: str = Field(description="venue name")


class SubscribeVenueTool(BaseAgentTool):
    name: str = "subscribe_venue"
    description: str = "useful when you need to subscribe a venue"
    args_schema: Optional[Type[BaseModel]] = SubscribeVenueToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        venue_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        venue_name = self._preporcess_input(venue_name)
        subscribe_venue(entity_name=self.entity_name, venue_name=venue_name)
        return f"\nSuccessfully subsribe venue {venue_name}\n"


class ListSubcriptionsTool(BaseAgentNoInputTool):
    name: str = "list_subscriptions"
    description: str = "useful when you need to list all subsciptions"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        subscriptions = list_subscriptions(entity_name=self.entity_name)
        msg = self._dataframe_to_msg(subscriptions)
        return f"\n{msg}\n"


class MarkPaperReadToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class MarkPaperReadTool(BaseAgentTool):
    name: str = "mark_paper_read"
    description: str = "useful when you need to mark a paper as read"
    args_schema: Optional[Type[BaseModel]] = MarkPaperReadToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        mark_paper_read(entity_name=self.entity_name, paper_id=paper_id)
        msg = f"Successfully mark paper {paper_id} read."
        return f"\n{msg}\n"


class SavePaperListToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class SavePaperListTool(BaseAgentTool):
    name: str = "save_paper_list"
    description: str = "useful when you need to save a paper to reading list"
    args_schema: Optional[Type[BaseModel]] = SavePaperListToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        save_paper_list(entity_name=self.entity_name, paper_id=paper_id)
        msg = f"Successfully add paper {paper_id} to reading list."
        return f"\n{msg}\n"


class ListReadingListTool(BaseAgentNoInputTool):
    name: str = "list_reading_list"
    description: str = "useful when you need to list the reading list"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        reading_list = list_reading_list(entity_name=self.entity_name)
        msg = self._dataframe_to_msg(reading_list)
        return f"\n{msg}\n"


class ListLatestReadingPapersToolInput(BaseModel):
    n: int = Field(description="number of papers")


class ListLatestReadingPapersTool(BaseAgentTool):
    name: str = "list_latest_reading_papers"
    description: str = (
        "useful when you need to find out latest reading papers, "
        "return a list of paper ids and titles for a given number."
    )
    args_schema: Optional[Type[BaseModel]] = ListLatestReadingPapersToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        df = list_latest_reading_papers(entity_name=self.entity_name, n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class ListRecentReadingPapersToolInput(BaseModel):
    date_time: str = Field(description="reading date time")


class ListRecentReadingPapersTool(BaseAgentTool):
    name: str = "list_recent_reading_papers"
    description: str = "useful when you need to find out all reading papers from a given date"
    args_schema: Optional[Type[BaseModel]] = ListRecentReadingPapersToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        date_time: str,
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

        df = list_recent_reading_papers(entity_name=self.entity_name, date_time=date_time)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
