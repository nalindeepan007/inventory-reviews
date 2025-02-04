from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc, and_
from fastapi import APIRouter, Depends, HTTPException
from app.db import getDb
from app.dbModel import ReviewHistory, Category
from app.schemas import CategoryReviewTrend, ReviewResponse
from app.logQueue import logAccess
from typing import List, Optional
from datetime import datetime
from openai import AsyncOpenAI 
import os




router = APIRouter()

openApiKey = os.getenv("OPENAPI_KEY")
openApiModel = os.getenv("OPENAPI_MODEL", "gpt-3.5-turbo") 
gptClient = AsyncOpenAI(
    api_key=f"{openApiKey}"
)



@router.get("/trends", response_model=list[CategoryReviewTrend])
async def get_ReviewTrends(db: AsyncSession = Depends(getDb)):
    try:
      


        subquery = (
        select(
            ReviewHistory.review_id,
            ReviewHistory.category_id,
            ReviewHistory.stars,
            ReviewHistory.created_at
        )
        .order_by(ReviewHistory.review_id, ReviewHistory.created_at.desc())
        .distinct(ReviewHistory.review_id)
        .subquery()
    )

        # avg star and total reviews in partic category
        query = (
            select(
                Category.id,
                Category.name,
                Category.description,
                func.avg(subquery.c.stars).label('average_stars'),
                func.count(subquery.c.review_id).label('total_reviews')
            )
            .join(subquery, Category.id == subquery.c.category_id)
            .group_by(Category.id)
            .order_by(func.avg(subquery.c.stars).desc())
            .limit(5)
            
        )


        result = await db.execute(query)
        trends = result.all()
        logAccess.delay("GET /reviews/trends")
        return trends
    except Exception as e:
      
        raise HTTPException(status_code=500, detail=f"Exception while getting trends : {str(e)}")



@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    category_id: int,
    cursor: Optional[datetime] = None,
    db: AsyncSession = Depends(getDb)
):
    
    try:
        recentReviewQuery = (
            select(
                ReviewHistory.review_id,
                func.max(ReviewHistory.created_at).label('max_created_at')
            )
            .filter(ReviewHistory.category_id == category_id)
            .group_by(ReviewHistory.review_id)
            .subquery()
        )
        
        # Build main query
        reviewQuery = select(ReviewHistory).join(
            recentReviewQuery,
            and_(
                ReviewHistory.review_id == recentReviewQuery.c.review_id,
                ReviewHistory.created_at == recentReviewQuery.c.max_created_at
            )
        )
        

        if cursor:
            reviewQuery = reviewQuery.where(ReviewHistory.created_at < cursor)
        
    
        reviewQuery = reviewQuery.order_by(desc(ReviewHistory.created_at)).limit(15)
        
    
        result = await db.execute(reviewQuery)
        reviews = result.scalars().all()
        
        
        finalReviews = []
        for review in reviews:
            if review.tone is None or review.sentiment is None:
                tone, sentiment = await analyzeViaGPT(review.text, review.stars)
                
        
                review.tone = tone
                review.sentiment = sentiment
                
            
                db.add(review)
                await db.commit()
                await db.refresh(review)
            
            
            reviewData = {
                'id': review.id,
                'text': review.text,
                'stars': review.stars,
                'review_id': review.review_id,
                'tone': review.tone,
                'sentiment': review.sentiment,
                'category_id': review.category_id,
                'created_at': review.created_at
            }
            finalReviews.append(reviewData)
        
        logAccess.delay(f"GET /reviews/?category_id={category_id}")
        
        return finalReviews
    except Exception as e:
      
        raise HTTPException(status_code=500, detail=f"Exception while getting review data : {str(e)}")




async def analyzeViaGPT(text: str, stars: int) -> tuple[str, str]:

    
    response = await gptClient.chat.completions.create(
        model=openApiModel,
        messages=[{
            "role": "system",
            "content": "Analyze the tone and sentiment of review and espond with two words: tone first, then sentiment. Use only these options - Tone: [formal, informal, neutral] Sentiment: [positive, negative, neutral]"
        }, {
            "role": "user",
            "content": f"Review text: {text}\nStars: {stars}/10"
        }]
    )
    tone, sentiment = response.choices[0].message.content.strip().split()
    return tone.lower(), sentiment.lower()
 
