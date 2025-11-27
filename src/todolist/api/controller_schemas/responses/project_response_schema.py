from datetime import datetime

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime

    class Config:
        orm_mode = True
