from prisma import Prisma
from fastapi import status, HTTPException, Request
from ...utils.sort_transacions import sort_transactions

prisma = Prisma()

async def get_Transactions(req:Request, skip:int, sort:str, category:str, name:str):
    await prisma.connect()
    query = {"userId":req.state.user}

    if category != "All Transactions":
        query["category"] = category
    
    if name != None:
        query["name"] = name
    
    items_sort = sort_transactions(sort)

    transactions = await prisma.transactions.find_many(
        where=dict(query),
        skip=skip,
        order= items_sort
    )

    if len(list(transactions)) <10:
        isLastPage = True
    else:
        isLastPage = False

    await prisma.disconnect()
    return {"success":True, "data":{"transactions":transactions, "isLastPage":isLastPage}}