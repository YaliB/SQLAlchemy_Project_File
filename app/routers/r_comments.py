from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/comments")
async def get_comments(request: Request):
    return {"message": "This is the comments routhe"}