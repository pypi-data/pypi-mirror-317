from typing import Union
from pandas.core.series import Series
from pandas.core.frame import DataFrame

from langchain_core.tools import BaseTool
from langchain_core.tools import ToolException
from langchain_core.language_models.chat_models import BaseChatModel


class BaseAgentTool(BaseTool):
    entity_name: str

    def _preporcess_input(self, s: str) -> str:
        # in some rare case, input may include the keyword
        # `Observation` in prompt.
        if isinstance(s, str):
            s = s.strip().replace("Observation:", "").replace("Observation", "").strip()
        return s

    def _raise_tool_error(self, err_msg: str) -> None:
        raise ToolException(err_msg)

    def _dataframe_to_msg(self, df: DataFrame) -> str:
        columns = df.columns.to_list()

        def _row_to_msg(row: Series) -> str:
            row_msg = []
            for col in columns:
                row_msg.append(f"{col}: {row[col]}")
            return ", ".join(row_msg)

        msg = "\n".join(df.apply(_row_to_msg, axis=1))

        return msg


class BaseAgentNoInputTool(BaseAgentTool):
    def _to_args_and_kwargs(self, tool_input: Union[str, dict]) -> tuple[tuple, dict]:
        return (), {}


class BaseAgentLLMTool(BaseAgentTool):
    llm: BaseChatModel
