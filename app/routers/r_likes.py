from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/likes")
async def get_likes(request: Request):
    return {"message": "This is the likes routhe"}