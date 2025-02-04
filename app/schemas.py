from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoryReviewTrend(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    average_stars: float
    total_reviews: int
    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    text: Optional[str]
    stars: int
    review_id: str
    tone: Optional[str]
    sentiment: Optional[str]
    category_id: int

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True