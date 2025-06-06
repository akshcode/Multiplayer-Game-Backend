from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

class DBModelMixin(DateTimeModelMixin):
    id: Optional[str] = None