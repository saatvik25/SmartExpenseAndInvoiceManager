from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate
from typing import List

class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: ExpenseCreate) -> Expense:
        db_obj = Expense(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_all(self) -> List[Expense]:
        return self.db.query(Expense).all()

    def get_by_month_year(self, month: int, year: int) -> List[Expense]:
        from sqlalchemy import extract
        return self.db.query(Expense).filter(
            extract('month', Expense.date) == month,
            extract('year', Expense.date) == year
        ).all()
