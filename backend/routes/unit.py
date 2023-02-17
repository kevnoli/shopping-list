from fastapi import APIRouter, status, Depends
from typing import List
from db import get_session

from models import Unit, UnitCreate, UnitRead, UnitUpdate
from controllers.unit import UnitController

router = APIRouter(prefix="/units", tags=["units"])

@router.get("", response_model=List[Unit])
async def fetch_units(db = Depends(get_session)):
    return UnitController.show(db)

@router.get("/{id}", response_model=UnitRead)
async def fetch_unit(id: int, db = Depends(get_session)):
    return UnitController.index(id, db)

@router.post("", response_model=UnitRead, status_code=status.HTTP_201_CREATED)
async def create_unit(unit: UnitCreate, db = Depends(get_session)):
    return UnitController.store(unit, db)

@router.patch("/{id}", response_model=UnitRead)
async def update_unit(id: int, unit: UnitUpdate, db = Depends(get_session)):
    return UnitController.update(id, unit, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_unit(id: int, db = Depends(get_session)):
    return UnitController.destroy(id, db)