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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GenericResponse)
async def CreatePot(data:CreatePot, req:Request):
    return await create_pot(req=req, data=data)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=GenericResponse)
async def DeletePot(id:int):
    return await delete_pot(id=id)

@router.get("/", status_code=status.HTTP_200_OK)
async def Getpots(req:Request, skip:Optional[int]=0):
    return await get_pots(req=req, skip=skip)

@router.patch("/", status_code=status.HTTP_200_OK, response_model=GenericResponse)
async def patch_pot(data:UpdatePot, req:Request, add:Optional[int]=None, subtract:Optional[int]=None):
    print(subtract)
    return await update_pot(data=data, req=req, add=add, subtract=subtract)