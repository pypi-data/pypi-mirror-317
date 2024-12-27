from langchain_core.tools import BaseToolkit

from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.tools.entity import (
    ListFollowsTool,
    ListFollowersTool,
    ListPopularEntitiesTool,
    FollowEntityTool,
    SubscribeVenueTool,
    ListSubcriptionsTool,
    MarkPaperReadTool,
    SavePaperListTool,
    ListReadingListTool,
    ListLatestReadingPapersTool,
    ListRecentReadingPapersTool,
)


class EntityToolkit(BaseToolkit):
    entity_name: str

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            ListFollowsTool(entity_name=self.entity_name),
            ListFollowersTool(entity_name=self.entity_name),
            ListPopularEntitiesTool(entity_name=self.entity_name),
            FollowEntityTool(entity_name=self.entity_name),
            SubscribeVenueTool(entity_name=self.entity_name),
            ListSubcriptionsTool(entity_name=self.entity_name),
            MarkPaperReadTool(entity_name=self.entity_name),
            SavePaperListTool(entity_name=self.entity_name),
            ListReadingListTool(entity_name=self.entity_name),
            ListLatestReadingPapersTool(entity_name=self.entity_name),
            ListRecentReadingPapersTool(entity_name=self.entity_name),
        ]
