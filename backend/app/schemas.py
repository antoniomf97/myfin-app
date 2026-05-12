from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


# Schema for creating a new transaction (incoming data from API)
class TransactionCreate(BaseModel):
    date: date
    type: str = Field(
        ..., pattern="^(income|expense)$"
    )  # Must be "income" or "expense"
    category: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)  # Must be greater than 0
    description: Optional[str] = None


# Schema for updating a transaction (all fields optional)
class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    type: Optional[str] = Field(None, pattern="^(income|expense)$")
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None


# Schema for API responses (includes the ID)
class TransactionResponse(BaseModel):
    id: int
    date: date
    type: str
    category: str
    amount: float
    description: Optional[str]

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


# Schema for analytics summary
class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# Schema for monthly breakdown
class MonthlyBreakdownItem(BaseModel):
    year: int
    month: int
    total_income: float
    total_expenses: float
    net_savings: float


# Schema for per category breakdown
class CategoryBreakdownItem(BaseModel):
    category: str
    type: str
    total: float
