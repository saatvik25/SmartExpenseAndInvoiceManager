from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseSummary
from app.services.expense_service import ExpenseService

router = APIRouter()
@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    *,
    db: Session = Depends(get_db),
    expense_in: ExpenseCreate
):
    """
    Create a new expense.
    """
    service = ExpenseService(db)
    return service.add_expense(expense_in)

@router.get("/", response_model=List[ExpenseResponse])
def read_expenses(
    db: Session = Depends(get_db)
):
    """
    Retrieve all expenses.
    """
    service = ExpenseService(db)
    return service.list_expenses()

@router.get("/summary", response_model=ExpenseSummary)
def get_summary(
    *,
    db: Session = Depends(get_db),
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100)
):
    """
    Get monthly spending summary grouped by category.
    """
    service = ExpenseService(db)
    return service.get_summary(month, year)
