from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CodeRunHistory(BaseModel):
    """A class to store code execution history with its result."""

    code: str = Field(description="The code that was run")
    result: str = Field(description="The result of the code execution")


class ToolParameter(BaseModel):
    """Schema for tool parameter following JSON Schema format"""

    type: str = Field(description="JSON Schema type of the parameter")
    description: str = Field(description="Description of the parameter")
    required: bool = Field(
        description="Whether the parameter is required", default=True
    )
    default: Optional[Any] = Field(description="Default value if any", default=None)


class ToolSchema(BaseModel):
    """Schema for tool/function following JSON Schema format"""

    name: str = Field(description="Name of the function")
    description: str = Field(description="Description of the function")
    parameters: Dict[str, ToolParameter] = Field(
        description="Dictionary of parameter schemas keyed by parameter name"
    )
    required: List[str] = Field(
        description="List of required parameter names", default_factory=list
    )
    returns: Dict[str, Any] = Field(
        description="Return type schema in JSON Schema format"
    )


class SavedTool(BaseModel):
    code: str = Field(description="Complete Python function implementation")
    tool_schema: ToolSchema = Field(description="Tool schema in JSON format")
