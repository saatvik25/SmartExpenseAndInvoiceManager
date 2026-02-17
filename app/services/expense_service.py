from sqlalchemy.orm import Session
from app.repositories.expense_repo import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseSummary, CategorySummary
from app.models.expense import Expense
from typing import List
from collections import defaultdict

class ExpenseService:
    def __init__(self, db: Session):
        self.repository = ExpenseRepository(db)

    def add_expense(self, expense_in: ExpenseCreate) -> Expense:
        # AI-Ready Hook: Categorization
        # if not expense_in.category:
        #     expense_in.category = self.ai_categorizer.predict(expense_in.title)
        
        return self.repository.create(expense_in)

    def list_expenses(self) -> List[Expense]:
        return self.repository.get_all()

    def get_summary(self, month: int, year: int) -> ExpenseSummary:
        expenses = self.repository.get_by_month_year(month, year)
        
        total_spent = sum(e.amount for e in expenses)
        
        category_map = defaultdict(float)
        for e in expenses:
            category_map[e.category] += e.amount
            
        breakdown = [
            CategorySummary(category=cat, total=amt) 
            for cat, amt in category_map.items()
        ]
        
        return ExpenseSummary(
            total_spent=total_spent,
            breakdown=breakdown
        )

    # Future AI methods
    # async def process_invoice_ocr(self, file_path: str):
    #     pass
