from typing import Type, Optional
from pydantic import BaseModel

from datetime import datetime
from langchain.callbacks.manager import CallbackManagerForToolRun

from docmesh_agent.tools.base import BaseAgentNoInputTool


class CurrentTimeTool(BaseAgentNoInputTool):
    name: str = "show_current_time"
    description: str = "useful when you need to know the current time"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Current time is: {current_time}"
        return f"\n{msg}\n"


class CurrentEntityName(BaseAgentNoInputTool):
    name: str = "show_current_entity_name"
    description: str = "useful when you need to know the current entity name"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        msg = f"Current entity name is: {self.entity_name}"
        return f"\n{msg}\n"
