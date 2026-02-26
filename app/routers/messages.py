from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/messages")
async def get_messages(request: Request):
    return {"message": "This is the messages routhe"}