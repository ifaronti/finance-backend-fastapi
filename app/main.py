from fastapi import FastAPI
from .routers.auth import auth_router
from .routers import transactions
from .routers import budgets
from .routers import pots
from .routers import bills

app = FastAPI()

app.include_router(auth_router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(pots.router)
app.include_router(bills.router)