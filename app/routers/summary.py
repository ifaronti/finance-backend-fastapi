from ..controllers.account_summary import account_summary
from fastapi import APIRouter, Depends, Request, status
from ..dependencies.token import verify_token


router = APIRouter(
    prefix="/summary",
    tags=["Account Summary"],
    dependencies=[Depends(verify_token)]
)

@router.get('', status_code=status.HTTP_200_OK)
def summary(req:Request):
    return account_summary(req=req)