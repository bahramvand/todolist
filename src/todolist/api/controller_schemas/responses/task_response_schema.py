from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: str
    project_id: str
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
