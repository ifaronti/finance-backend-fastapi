from fastapi import FastAPI, Request
from .routers import auth
from .routers import transactions
from .routers import budgets
from .routers import pots
from .routers import bills
from prisma import Prisma
from .controllers.account_summary import account_summary

app = FastAPI()
prisma = Prisma()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(pots.router)
app.include_router(bills.router)

    