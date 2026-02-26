from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/groups")
async def get_groups(request: Request):
    return {"message": "This is the groups routhe"}