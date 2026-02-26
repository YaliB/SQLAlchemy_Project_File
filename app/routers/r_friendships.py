from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/friendships")
async def get_friendships(request: Request):
    return {"message": "This is the friendships routhe"}