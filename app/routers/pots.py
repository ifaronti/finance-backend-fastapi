from fastapi import APIRouter, Request, Depends, status
from ..controllers.pots.create_pot import create_pot
from ..controllers.pots.delete_pot import delete_pot
from ..controllers.pots.get_pots import get_pots
from ..controllers.pots.update_pot import update_pot
from ..dependencies.token import verify_token
from ..utils.models import CreatePot, UpdatePot, GenericResponse
from typing import Optional

router = APIRouter(
    prefix="/pots",
    tags=["Pots"],
    dependencies=[Depends(verify_token)]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=GenericResponse)
def add_pot(data:CreatePot, req:Request):
    return create_pot(req=req, data=data)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=GenericResponse)
def DeletePot(id:int, req:Request):
    return delete_pot(id=id, req=req)

@router.get("", status_code=status.HTTP_200_OK)
def Getpots(req:Request, skip:Optional[int]=0):
    return get_pots(req=req, skip=skip)

@router.patch("/pot/modify", status_code=status.HTTP_200_OK, response_model=GenericResponse)
def edit_pot(data:UpdatePot, req:Request, add:Optional[int]=None, subtract:Optional[int]=None):
    return update_pot(data=data, req=req, add=add, subtract=subtract)