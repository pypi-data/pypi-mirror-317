import json

from typing import Any

from sqlalchemy import Column, Integer, Text

try:
    from sqlalchemy.orm import declarative_base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base

from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_community.chat_message_histories.sql import BaseMessageConverter, SQLChatMessageHistory


def create_message_model(table_name: str, DynamicBase: Any) -> Any:
    class Message(DynamicBase):
        __tablename__ = table_name
        id = Column(Integer, primary_key=True)
        entity_name = Column(Text)
        session_id = Column(Text)
        message = Column(Text)

    return Message


class DocmeshMessageConverter(BaseMessageConverter):
    def __init__(self, table_name: str) -> None:
        self.model_class = create_message_model(table_name, declarative_base())

    def from_sql_model(self, sql_message: Any) -> BaseMessage:
        return messages_from_dict([json.loads(sql_message.message)])[0]

    def to_sql_model(self, message: BaseMessage, session_id: str, entity_name: str) -> Any:
        return self.model_class(
            session_id=session_id,
            entity_name=entity_name,
            message=json.dumps(message_to_dict(message)),
        )

    def get_sql_model_class(self) -> Any:
        return self.model_class


class DocmeshMessageHistory(SQLChatMessageHistory):
    def __init__(
        self,
        session_id: str,
        entity_name: str,
        connection_string: str,
        table_name: str = "message_store",
        **kwargs,
    ) -> None:
        self.entity_name = entity_name

        custom_message_converter = DocmeshMessageConverter(table_name)
        super().__init__(
            session_id,
            connection_string,
            table_name=table_name,
            custom_message_converter=custom_message_converter,
            **kwargs,
        )

    def add_message(self, message: BaseMessage) -> None:
        with self.Session() as session:
            session.add(self.converter.to_sql_model(message, self.session_id, self.entity_name))
            session.commit()
