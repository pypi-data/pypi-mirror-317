from typing import List
import requests
from ..schemas import SavedTool
from .base import StorageAdapter, ToolStatus


class APIStorageAdapter(StorageAdapter):
    def __init__(self, api_base_url: str):
        if not api_base_url:
            api_base_url = "http://localhost:3000"
        self.api_base_url = api_base_url.rstrip("/")

    def load_tools(self) -> List[SavedTool]:
        response = requests.get(f"{self.api_base_url}/api/tools")
        response.raise_for_status()
        tools = response.json()
        return [SavedTool(**tool) for tool in tools]

    def add_tool(self, uuid: str, tool: SavedTool, status=ToolStatus.ACTIVE):
        response = requests.post(
            f"{self.api_base_url}/api/tools",
            json={
                "uuid": str(uuid),
                "code": tool.code,
                "tool_schema": tool.tool_schema.model_dump(),
                "status": status.value,
            },
        )
        response.raise_for_status()
        return str(uuid)

    def add_code_run_history(self, uuid: str, code: str, result: str):
        response = requests.post(
            f"{self.api_base_url}/api/code-run-histories",
            json={"uuid": str(uuid), "code": code, "result": result},
        )
        response.raise_for_status()
        return str(uuid)

    def add_suggestion(self, uuid: str, code_run_history_uuid: str, tool_uuid: str):
        response = requests.post(
            f"{self.api_base_url}/api/suggestions",
            json={
                "uuid": str(uuid),
                "code_run_history_uuid": str(code_run_history_uuid),
                "tool_uuid": str(tool_uuid),
            },
        )
        response.raise_for_status()
        return str(uuid)
