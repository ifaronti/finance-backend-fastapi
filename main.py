from fastapi import FastAPI
from app.routers import auth
from app.routers import transactions
from app.routers import budgets
from app.routers import pots
from app.routers import bills
from app.routers import summary
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization", "X-Custom-Header"] 
)

app.include_router(auth.router)
app.include_router(summary.router)
app.include_router(transactions.router)
app.include_router(bills.router)
app.include_router(budgets.router)
app.include_router(pots.router)

@app.get('/')
def welcome_page():
    return "WELCOME TO MY API. ADD '/docs' TO THE URL TO CHECK IT OUT"

    
handler = Mangum(app)

# find . -type d -name __pycache__ -exec rm -r {} \+   *command cleans pycache from project