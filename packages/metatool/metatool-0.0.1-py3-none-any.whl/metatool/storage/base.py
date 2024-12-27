from abc import ABC, abstractmethod
from typing import List
from ..schemas import SavedTool
from enum import Enum


class ToolStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUGGESTED = "SUGGESTED"
    DECLINED = "DECLINED"


class StorageAdapter(ABC):
    @abstractmethod
    def load_tools(self) -> List[SavedTool]:
        """Load saved tools from storage"""
        pass

    @abstractmethod
    def add_tool(self, uuid: str, tool: SavedTool, status=ToolStatus.ACTIVE) -> str:
        """Add a single tool to storage"""
        pass

    @abstractmethod
    def add_code_run_history(self, uuid: str, code: str, result: str) -> str:
        """Add a code run history entry to storage"""
        pass

    @abstractmethod
    def add_suggestion(
        self, uuid: str, code_run_history_uuid: str, tool_uuid: str
    ) -> str:
        """Add a suggestion of tool based on a code run history to storage"""
        pass
