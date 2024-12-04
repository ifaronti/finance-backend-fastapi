from fastapi import APIRouter, Depends, Request, status
from ..controllers.budgets.create_budget import create_budget
from ..controllers.budgets.delete_budget import delete_budget
from ..controllers.budgets.get_budgets import get_budgets
from ..controllers.budgets.update_budget import update_budget
from ..dependencies.token import verify_token
from ..utils.models import CreateBudget, UpdateBudget, GenericResponse
from typing import Optional


router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
    dependencies=[Depends(verify_token)]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GenericResponse)
async def createBudget(data:CreateBudget, req:Request):
    return await create_budget(data, req)

@router.delete("/budget/{id}", status_code=status.HTTP_200_OK, response_model=GenericResponse)
async def deleteBudget(id:int):
    return await delete_budget(id)

@router.get("/", status_code=status.HTTP_200_OK)
async def getBudgets(req:Request, skip:Optional[int]=0):
    return await get_budgets(req=req, skip=skip)

@router.patch("/budget", status_code=status.HTTP_200_OK, response_model=GenericResponse)
async def updateBudget(data:UpdateBudget, req:Request):
    return await update_budget(data=data, req=req)