from fastapi import FastAPI, Request
from .routers import auth
from .routers import transactions
from .routers import budgets
from .routers import pots
from .routers import bills
from prisma import Prisma
from .controllers.account_summary import account_summary
import json

# from mangum import Mangum

app = FastAPI()
prisma = Prisma()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(pots.router)
app.include_router(bills.router)


# @app.get('/category')
# async def create_categories():
#     with open("placeholders.json") as file:
#         data = json.load(file)
    
#     await prisma.connect()
#     await prisma.category.create_many(data=data["categories"])
#     await prisma.disconnect()
    