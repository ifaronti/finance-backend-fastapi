from fastapi import APIRouter, Depends, Request, status
from ..controllers.transactions.get_transactions import get_Transactions
from ..dependencies.token import verify_token
from typing import Optional

router = APIRouter(
    prefix="/transactions", 
    tags=["Transactions"],
    dependencies=[Depends(verify_token)]
)

description = ('Get transactions by name, or categories and sort result by name, amount or date. You can also skip result by 10')

@router.get('/', status_code=status.HTTP_200_OK, description=description)
async def transactions(req:Request, skip:int, sort:str, category:str, name:Optional[str]=None):
    return await get_Transactions(req, skip, sort, category, name)