from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import get_db
from app.models import Transaction
from app.schemas import SummaryResponse, MonthlyBreakdownItem

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """Get total income, total expenses, and net savings for a given period."""

    def base_query(transaction_type: str):
        q = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == transaction_type
        )
        if start_date:
            q = q.filter(Transaction.date >= start_date)
        if end_date:
            q = q.filter(Transaction.date <= end_date)
        return q.scalar() or 0.0

    total_income = base_query("income")
    total_expenses = base_query("expense")

    return SummaryResponse(
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=total_income - total_expenses,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/monthly", response_model=list[MonthlyBreakdownItem])
def get_monthly_breakdown(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """Get income, expenses, and net savings grouped by month."""

    def monthly_totals(transaction_type: str) -> dict[tuple, float]:
        q = db.query(
            func.strftime("%Y", Transaction.date).label("year"),
            func.strftime("%m", Transaction.date).label("month"),
            func.sum(Transaction.amount).label("total"),
        ).filter(Transaction.type == transaction_type)
        if start_date:
            q = q.filter(Transaction.date >= start_date)
        if end_date:
            q = q.filter(Transaction.date <= end_date)
        rows = q.group_by("year", "month").all()
        return {(int(r.year), int(r.month)): r.total for r in rows}

    income_by_month = monthly_totals("income")
    expense_by_month = monthly_totals("expense")

    all_months = sorted(income_by_month.keys() | expense_by_month.keys())

    return [
        MonthlyBreakdownItem(
            year=year,
            month=month,
            total_income=income_by_month.get((year, month), 0.0),
            total_expenses=expense_by_month.get((year, month), 0.0),
            net_savings=income_by_month.get((year, month), 0.0)
            - expense_by_month.get((year, month), 0.0),
        )
        for year, month in all_months
    ]
