from ..controllers.account_summary import account_summary
from fastapi import APIRouter, Depends, Request, status
from ..dependencies.token import verify_token


router = APIRouter(
    prefix="/summary",
    tags=["Account Summary"],
    dependencies=[Depends(verify_token)]
)

@router.get('/', status_code=status.HTTP_200_OK)
async def summary(req:Request):
    return await account_summary(req=req)