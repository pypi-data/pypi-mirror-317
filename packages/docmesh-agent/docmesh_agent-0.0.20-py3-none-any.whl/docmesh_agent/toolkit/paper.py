from langchain_core.tools import BaseToolkit
from langchain_core.language_models.chat_models import BaseChatModel

from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.tools.paper import (
    AddPaperTool,
    GetPaperIdTool,
    GetPaperDetailsTool,
    GetPaperPDFTool,
    ReadWholePDFTool,
    ReadPartialPDFTool,
    ExtractFiguresTool,
    PaperPosterTool,
)


class PaperToolkit(BaseToolkit):
    entity_name: str
    llm: BaseChatModel

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            AddPaperTool(entity_name=self.entity_name),
            GetPaperIdTool(entity_name=self.entity_name),
            GetPaperDetailsTool(entity_name=self.entity_name),
            GetPaperPDFTool(entity_name=self.entity_name),
            ReadWholePDFTool(entity_name=self.entity_name),
            ReadPartialPDFTool(entity_name=self.entity_name),
            ExtractFiguresTool(entity_name=self.entity_name),
            PaperPosterTool(entity_name=self.entity_name, llm=self.llm),
        ]
