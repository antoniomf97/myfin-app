from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate, TransactionResponse

# Create router for transactions
router = APIRouter(prefix="/transactions", tags=["transactions"])


# CREATE: Add new transaction
@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction (income or expense)"""
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# READ: Get all transactions
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """
    Get all transactions with optional filters:
    - type: Filter by 'income' or 'expense'
    - category: Filter by category (exact match, case-sensitive)
    - start_date: Filter transactions from this date onwards (YYYY-MM-DD)
    - end_date: Filter transactions up to this date (YYYY-MM-DD)
    - skip: Number of records to skip (for pagination)
    - limit: Maximum number of records to return (max 100)
    """
    query = db.query(Transaction)

    # Apply filters if provided
    if type:
        query = query.filter(Transaction.type == type)

    if category:
        query = query.filter(Transaction.category == category)

    if start_date:
        query = query.filter(Transaction.date >= start_date)

    if end_date:
        query = query.filter(Transaction.date <= end_date)

    # Order by date (newest first) and apply pagination
    transactions = (
        query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    )

    return transactions


# READ-ID: Get single transaction by ID
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(
            status_code=404, detail=f"Transaction with ID {transaction_id} not found"
        )

    return transaction


# UPDATE-ID: Update transaction by ID
@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing transaction"""
    # Find the transaction
    db_transaction = (
        db.query(Transaction).filter(Transaction.id == transaction_id).first()
    )

    if not db_transaction:
        raise HTTPException(
            status_code=404, detail=f"Transaction with ID {transaction_id} not found"
        )

    # Update only the fields that were provided (exclude_unset=True)
    update_data = transaction_update.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)

    return db_transaction


# DELETE-ID: Delete transaction by ID
@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction"""
    db_transaction = (
        db.query(Transaction).filter(Transaction.id == transaction_id).first()
    )

    if not db_transaction:
        raise HTTPException(
            status_code=404, detail=f"Transaction with ID {transaction_id} not found"
        )

    db.delete(db_transaction)
    db.commit()

    return None  # 204 No Content response
