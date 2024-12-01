from prisma import Prisma
from fastapi import Request, HTTPException, status

prisma = Prisma()


async def account_summary(req:Request):
    # try:
    await prisma.connect()
    glimpse = await prisma.query_raw(f""" """)
    
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="prisma error")
    # finally:
    #     
    await prisma.disconnect()
    return glimpse