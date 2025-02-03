from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from fastapi import APIRouter, Depends, Query, HTTPException
from app.db import getDb
from app.dbModel import ReviewHistory, Category
from app.schemas import CategoryTrend




router = APIRouter()



@router.get("/trends", response_model=list[CategoryTrend])
async def list_files(db: AsyncSession = Depends(getDb)):
    try:
        # result = await db.execute(select(ReviewHistory))


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
        
        return trends
    except Exception as e:
        print(f"$$$$------ error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Exception while getting trends from db : {str(e)}")



@router.get("/getFile")
async def getFileFromStore(db: AsyncSession = Depends(getDb), fileId: str = Query(
        ...,
        title="fileId",
        description="file id/name for file stored in minIO storage"
    )):
  
    try:
        url = "example"
        
        return {"result": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception while getting URL from minio store: {str(e)}")