from datetime import datetime
from uuid import uuid4
from typing import List
from sqlalchemy import (
    create_engine,
    Column,
    String,
    JSON,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..schemas import SavedTool
from .base import StorageAdapter, ToolStatus
import os

Base = declarative_base()


class ToolModel(Base):
    __tablename__ = "tools"

    uuid = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code = Column(String)
    tool_schema = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    status = Column(
        SQLAlchemyEnum(ToolStatus), default=ToolStatus.ACTIVE, nullable=False
    )


class CodeRunHistoryModel(Base):
    __tablename__ = "code_run_histories"

    uuid = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code = Column(String)
    result = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now)


class SuggestionModel(Base):
    __tablename__ = "suggestions"

    uuid = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code_run_history_uuid = Column(
        String, ForeignKey("code_run_histories.uuid"), nullable=False
    )
    tool_uuid = Column(String, ForeignKey("tools.uuid"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    accepted_at = Column(DateTime(timezone=True))
    declined_at = Column(DateTime(timezone=True))


class SQLiteStorageAdapter(StorageAdapter):
    def __init__(self, database_path: str):
        if not database_path:
            raise ValueError("Database path is not set")

        # Create directory if it doesn't exist
        database_dir = os.path.dirname(database_path)
        if database_dir and not os.path.exists(database_dir):
            os.makedirs(database_dir)

        database_url = f"sqlite:///{database_path}"
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def load_tools(self) -> List[SavedTool]:
        """Load saved tools from storage"""
        session = self.Session()
        try:
            tools = session.query(ToolModel).all()
            return [
                SavedTool.model_validate(
                    {"code": tool.code, "tool_schema": tool.tool_schema}
                )
                for tool in tools
            ]
        finally:
            session.close()

    def add_tool(self, uuid: str, tool: SavedTool, status=ToolStatus.ACTIVE) -> str:
        """Add a single tool to storage"""
        session = self.Session()
        try:
            tool_data = tool.model_dump()
            db_tool = ToolModel(
                uuid=str(uuid),
                code=tool_data["code"],
                tool_schema=tool_data["tool_schema"],
                status=status,
            )
            session.add(db_tool)
            session.commit()
            return str(uuid)
        finally:
            session.close()

    def add_code_run_history(self, uuid: str, code: str, result: str) -> str:
        """Add a code run history entry to storage"""
        session = self.Session()
        try:
            history = CodeRunHistoryModel(uuid=str(uuid), code=code, result=result)
            session.add(history)
            session.commit()
            return str(uuid)
        finally:
            session.close()

    def add_suggestion(
        self, uuid: str, code_run_history_uuid: str, tool_uuid: str
    ) -> str:
        """Add a suggestion of tool based on a code run history to storage"""
        session = self.Session()
        try:
            suggestion = SuggestionModel(
                uuid=str(uuid),
                code_run_history_uuid=code_run_history_uuid,
                tool_uuid=tool_uuid,
            )
            session.add(suggestion)
            session.commit()
            return str(uuid)
        finally:
            session.close()
