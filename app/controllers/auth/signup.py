from prisma import Prisma
from ...dependencies.password_manager import hash_password
from ...dependencies.placeholders import account_balance, placeholders
import asyncio
from fastapi import HTTPException, status
from ...utils.models import Register

prisma = Prisma()

async def signup(user_details:Register):
    queryDetails = dict(user_details).copy()
    hashed_pass = hash_password(user_details.password)
    balances = account_balance()
    queryDetails.update({
            "income":balances["income"], 
            "expenses":balances["expenses"],
            "balance":balances["current"],
            "password":hashed_pass
        })
    try:
        await prisma.connect()
        already_user = await prisma.user.find_first(where={"email":queryDetails["email"]})

        if(already_user):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail="User already exists"
                                )
        user = await prisma.user.create(data = queryDetails)
        holder_data = placeholders(user.id)

        await asyncio.gather(
            prisma.transactions.create_many(data=holder_data["transactions"]),
            prisma.budgets.create_many(data=holder_data["budgets"]),
            prisma.pots.create_many(data=holder_data["pots"]),
            prisma.bills.create_many(data=holder_data["bills"]),
            # return_exceptions=True,
        )
    finally:
        await prisma.disconnect()

    return {"success":True, "message":"Account created"}

if __name__ == '__main__':
    asyncio.run(signup())