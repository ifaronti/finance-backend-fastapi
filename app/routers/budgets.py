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
def createBudget(data:CreateBudget, req:Request):
    return create_budget(data, req)

@router.delete("/budget/{id}", status_code=status.HTTP_200_OK, response_model=GenericResponse)
def deleteBudget(id:int, req:Request):
    return delete_budget(id, req=req)

@router.get("/", status_code=status.HTTP_200_OK)
def getBudgets(req:Request, skip:Optional[int]=0):
    return get_budgets(req=req, skip=skip)

@router.patch("/budget", status_code=status.HTTP_200_OK, response_model=GenericResponse)
def updateBudget(data:UpdateBudget, req:Request):
    return update_budget(data=data, req=req)