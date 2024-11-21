from prisma import Prisma
from fastapi import Request, status, HTTPException
from ...utils.models import UpdatePot
from typing import Optional

prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

async def update_pot(req:Request, data:UpdatePot, add:Optional[int]=None, subtract:Optional[int]=None):
    data_copy = dict(data).copy()
    data_copy["userId"] = req.state.user
    if add:
        balance_query = {"increment":add}
    if subtract:
        balance_query = {"decrement":subtract}
    try:
        await prisma.connect()
        if add or subtract:
            await prisma.user.update(where={"id":req.state.user}, 
                                 data={"balance":balance_query})
            
        await prisma.pot.update(
            data=data_copy, 
            where={"potId":data_copy["potId"], "userId":req.state.user}
        )
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()
    
    return {"success":True, "message":"Pot updated."}