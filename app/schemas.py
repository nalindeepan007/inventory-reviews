from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoryTrend(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    average_stars: float
    total_reviews: int
    class Config:
        from_attributes = True