from .base import StorageAdapter
from .sqlite_storage import SQLiteStorageAdapter
from .api_storage import APIStorageAdapter
import os
from ..schemas import SavedTool
from .base import ToolStatus
from typing import Optional
from ..config import MetaToolConfig

__all__ = [
    "StorageAdapter",
    "SQLiteStorageAdapter",
    "APIStorageAdapter",
    "load_tools",
    "get_storage_adapter",
    "add_tool",
    "add_code_run_history",
    "add_suggestion",
]


def get_storage_adapter(config: Optional[MetaToolConfig] = None) -> StorageAdapter:
    """Get the appropriate storage adapter based on configuration"""
    if config is None:
        config = MetaToolConfig()

    if config.api_key:
        return APIStorageAdapter(config.api_key)
    
    # Use SQLite by default if no API key is provided
    database_path = os.path.join(config.root_dir, config.database_path)
    return SQLiteStorageAdapter(database_path)


# Create a default storage adapter instance
_default_storage = get_storage_adapter()


def load_tools():
    return _default_storage.load_tools()


def add_tool(uuid: str, tool: SavedTool, status: ToolStatus) -> str:
    """Add a new tool to storage with the given UUID"""
    return _default_storage.add_tool(uuid, tool, status)


def add_code_run_history(uuid: str, code: str, result: str):
    """Add a code run history entry to storage"""
    return _default_storage.add_code_run_history(uuid, code, result)


def add_suggestion(uuid: str, code_run_history_uuid: str, tool_uuid: str):
    """Add a suggestion of tool based on a code run history to storage"""
    return _default_storage.add_suggestion(uuid, code_run_history_uuid, tool_uuid)
