from langchain_core.tools import BaseToolkit
from langchain_core.language_models.chat_models import BaseChatModel

from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.tools.cypher import (
    GenerateCypherTool,
    ExecuteCypherTool,
)


class CypherToolkit(BaseToolkit):
    entity_name: str
    llm: BaseChatModel

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            GenerateCypherTool(entity_name=self.entity_name, llm=self.llm),
            ExecuteCypherTool(entity_name=self.entity_name),
        ]
