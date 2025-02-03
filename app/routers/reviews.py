from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException
from app.db import getDb
from app.dbModel import ReviewHistory





router = APIRouter()



@router.get("/trends")
async def list_files(db: AsyncSession = Depends(getDb)):
    try:
        result = await db.execute(select(ReviewHistory))
        files = result.scalars().all()
        
        return [
            {
                "file_id": file.id,
                "filename": file.filename,
                "uploaded_at": file.uploaded_at,
                "file_size": file.size
            } for file in files
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception while getting Files from DB : {str(e)}")



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