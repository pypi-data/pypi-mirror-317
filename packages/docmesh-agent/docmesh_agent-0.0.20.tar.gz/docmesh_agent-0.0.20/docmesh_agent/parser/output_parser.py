import json

from typing import Union

from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.output_parsers import ReActSingleInputOutputParser


class ReActInputOutputParser(ReActSingleInputOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        agent_action = super().parse(text)
        # we only further parse the AgentAction
        if isinstance(agent_action, AgentAction):
            # try use json to parse the tool input
            try:
                tool_input_dict = json.loads(agent_action.tool_input.replace("'", '"'))
                agent_action.tool_input = tool_input_dict
            except Exception:
                # we preserve the original tool_input
                pass
        return agent_action
