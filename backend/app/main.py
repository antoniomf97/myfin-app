from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from app.database import engine, Base, get_db
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate, TransactionResponse

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API", version="1.0.0")

# CORS configuration (allows React frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Create React App default
        "http://localhost:5173",  # Vite default
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Finance Tracker API is running"}


# CREATE: Add new transaction
@app.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction (income or expense)"""
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# READ: Get all transactions
@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all transactions with pagination"""
    transactions = (
        db.query(Transaction)
        .order_by(Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transactions


# READ: Get single transaction by ID
@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(
            status_code=404, detail=f"Transaction with ID {transaction_id} not found"
        )

    return transaction


# UPDATE: Update transaction by ID
@app.put("/transactions/{transaction_id}", response_model=TransactionResponse)
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


# DELETE: Delete transaction by ID
@app.delete("/transactions/{transaction_id}", status_code=204)
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
