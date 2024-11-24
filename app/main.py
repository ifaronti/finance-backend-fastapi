from fastapi import FastAPI
from .routers import auth
from .routers import transactions
from .routers import budgets
from .routers import pots
from .routers import bills
# from mangum import Mangum


app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(pots.router)
app.include_router(bills.router)



# lambda_handler = Mangum(app=app, lifespan="off")