from typing import Optional
from pydantic import BaseModel


class MetaToolConfig(BaseModel):
    """Configuration for MetaTool"""

    openai_api_key: Optional[str] = None
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0
    verbose: bool = False
    root_dir: str = "./metatool_tmp"
    api_key: Optional[str] = None  # API key for storage service
    database_path: str = "metatool.db"  # SQLite database path relative to root_dir
