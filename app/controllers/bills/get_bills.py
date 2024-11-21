from fastapi import HTTPException, Request, status
from typing import Optional
from prisma import Prisma
from ...utils.sort_transacions import sort_transactions

prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

async def get_bills(req:Request, skip:Optional[int]=0, name:Optional[str]=None, 
                    sort:Optional[str]="Latest"):
    
    item_sort = sort_transactions(sort, createdAt=True)
    query = {"userId":req.state.user}

    if name != None:
        query["name"] = name

    try:
        await prisma.connect()
        bills = await prisma.bills.find_many(where=query, skip=skip, order=item_sort)
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()
    
    bills_copy = list(bills)

    if len(bills_copy) < 10:
        isLastPage = True
    else:
        isLastPage = False
    
    return {"success":True, "data":bills_copy, "isLastPage":isLastPage}