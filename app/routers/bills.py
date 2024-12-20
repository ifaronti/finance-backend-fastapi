from fastapi import APIRouter, Request, Depends, status
from ..dependencies.token import verify_token
from ..utils.models import CreateBill, GenericResponse
from ..controllers.bills.create_bill import create_bill
from ..controllers.bills.delete_bill import delete_bill
from ..controllers.bills.get_bills import get_bills
from typing import Optional

router = APIRouter(
    prefix="/bills",
    tags=["Bills"],
    dependencies=[Depends(verify_token)]
)

getBills_description = "Get bills in multitude of 10, skip by 10 and or get by bill's name"

@router.post("", status_code=status.HTTP_201_CREATED, response_model=GenericResponse, description="Add a new bill")
def new_bill(data:CreateBill, req:Request):
    return create_bill(data=data, req=req)

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=GenericResponse, description="Delete a bill")
def remove_bill(id:int, req:Request):
    return delete_bill(id=id, req=req)

@router.get("/all", status_code=status.HTTP_200_OK, description=getBills_description)
def getBills(req:Request, skip:Optional[int]=0, name:Optional[str]=None):
    return get_bills(req=req, skip=skip, name=name)