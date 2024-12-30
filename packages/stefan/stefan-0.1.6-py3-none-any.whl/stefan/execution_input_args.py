from pathlib import Path

from pydantic import BaseModel

class ExecutionInputArgs(BaseModel):
    task: str
    working_dir: Path
