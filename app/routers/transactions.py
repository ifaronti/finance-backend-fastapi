from fastapi import APIRouter, Depends, Request, status, Query
from ..controllers.transactions.get_transactions import get_Transactions
from ..dependencies.token import verify_token
from typing import Optional
from enum import Enum

router = APIRouter(
    prefix="/transactions", 
    tags=["Transactions"],
    dependencies=[Depends(verify_token)]
)

class Category(str, Enum):
        All = "All"
        Education= "Education",
        Bills= "Bills",
        Groceries= "Groceries",
        Dining = "Dining Out",
        Transportation = "Transportation",
        Personal = "Personal Care", 
        General = "General",
        Lifestyle = "Lifestyle",
        Shopping = "Shopping",
        Entertainment = "Entertainment",

class Sort(str, Enum):
      Latest = "Latest"
      Oldest = "Oldest"
      Highest = "Highest"
      Lowest = "Lowest"
      ZA = "Z-A"
      AZ = "A-Z"

description = ("""Get transactions by name, or categories and sort result by name, 
                amount or date. You can also skip by a given number. The limit per 
               request is 10
               """)

@router.get('', status_code=status.HTTP_200_OK, description=description)
def transactions(
                req:Request, 
                skip:int, 
                sort:Sort, 
                category:Category, 
                name:Optional[str]=None
            ):
    match(sort):
          case "AZ":
                sort = 'A-Z'
          case "ZA":
                sort = 'Z-A'


    return get_Transactions(req=req, skip=skip, sort=sort, category=category, name=name)