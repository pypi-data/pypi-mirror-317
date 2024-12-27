from langchain_core.tools import BaseToolkit

from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.tools.common import CurrentTimeTool, CurrentEntityName


class CommonToolkit(BaseToolkit):
    entity_name: str

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            CurrentTimeTool(entity_name=self.entity_name),
            CurrentEntityName(entity_name=self.entity_name),
        ]
