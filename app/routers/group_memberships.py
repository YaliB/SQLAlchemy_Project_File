from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/group_memberships")
async def get_group_memberships(request: Request):
    return {"message": "This is the group_memberships routhe"}