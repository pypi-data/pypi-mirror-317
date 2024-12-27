import os

from typing import Type, Optional
from pydantic import BaseModel, Field

from langchain import hub
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.callbacks.manager import CallbackManagerForToolRun

from docmesh_core.db.neo.common import safe_execute_cypher_query, SafeExecutionException
from docmesh_agent.tools.template import NEOMODEL_TEMPLATE
from docmesh_agent.tools.base import BaseAgentTool, BaseAgentLLMTool
from docmesh_agent.embeddings.embeddings import query_embeddings


class Cypher(BaseModel):
    cypher_query: str = Field(description="generated cypher query")
    embeddings_keyword: str = Field(description="keyword to generate embeddings further")


class GenerateCypherToolInput(BaseModel):
    question: str = Field(description="question")


class GenerateCypherTool(BaseAgentLLMTool):
    name: str = "generate_cypher"
    description: str = (
        "useful when you need to generate a cypher from a complicated question, "
        "this can be especially helpful when dealing with a task to find out "
        "relationship between entities, papers, collections and venues"
    )
    args_schema: Optional[Type[BaseModel]] = GenerateCypherToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        question: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        question = self._preporcess_input(question)

        prompt = hub.pull(os.getenv("DOCMESH_AGENT_CYPHER_PROMPT"))
        prompt = prompt.partial(entity_name=self.entity_name)
        parser = PydanticOutputParser(pydantic_object=Cypher)
        fixing_paresr = OutputFixingParser.from_llm(parser=parser, llm=self.llm)

        prompt = prompt.partial(
            neomodel_template=NEOMODEL_TEMPLATE,
            format_instructions=parser.get_format_instructions(),
        )
        chain = prompt | self.llm | parser

        try:
            res = chain.invoke({"input": question})
        except OutputParserException as e:
            res = fixing_paresr.parse(e.llm_output)

        msg = f"cypher query: {res.cypher_query}, embeddings keywords: {res.embeddings_keyword}"

        return f"\n{msg}\n"


class ExecuteCypherToolInput(BaseModel):
    cypher_query: str = Field(description="cypher query to execute")
    embeddings_keyword: str = Field(description="keyword to generate embeddings further")


class ExecuteCypherTool(BaseAgentTool):
    name: str = "execute_cypher"
    description: str = "useful when you need to execute a cypher"
    args_schema: Optional[Type[BaseModel]] = ExecuteCypherToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        cypher_query: str,
        embeddings_keyword: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        cypher_query = self._preporcess_input(cypher_query)
        embeddings_keyword = self._preporcess_input(embeddings_keyword)

        if embeddings_keyword != "" and "$embeddings" in cypher_query:
            embeddings = query_embeddings(embeddings_keyword)
            params = {"embeddings": embeddings}
        else:
            params = None

        try:
            df = safe_execute_cypher_query(query=cypher_query, params=params)
        except SafeExecutionException as e:
            self._raise_tool_error(
                f"Can not execute cypher query {cypher_query} with error: {e}.\n "
                f"Please use another tool to achieve your goal."
            )
        except Exception as e:
            self._raise_tool_error(f"Failed to execute cypher query {cypher_query} with error: {e}.")

        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
