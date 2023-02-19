from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select
from models import Unit, UnitCreate, UnitUpdate


class UnitController():
    @classmethod
    def index(self, id: int, db: Session) -> Unit:
        obj = db.get(Unit, id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"Unit not found with id {id}.")
        return obj

    @classmethod
    def show(self, db: Session) -> List[Unit]:
        statement = select(Unit)
        return db.exec(statement).all()

    @classmethod
    def store(self, data: UnitCreate, db: Session) -> Unit:
        unit = Unit.from_orm(data)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit

    @classmethod
    def update(self, id: int, data: UnitUpdate, db: Session) -> Unit:
        unit = db.get(Unit, id)
        if not unit:
            raise HTTPException(
                status_code=404, detail=f"Unit not found with id {id}.")
        data_dict = data.dict(exclude_unset=True)
        data_dict["updated_at"] = datetime.utcnow()
        for k, v in data_dict.items():
            setattr(unit, k, v)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit

    @classmethod
    def destroy(self, id: int, db: Session) -> None:
        obj = db.get(Unit, id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"Unit not found with id {id}.")
        db.delete(obj)
        db.commit()