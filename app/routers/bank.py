from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import cast
from app.dependencies import get_db
from app.utils.bank_adapter import mock_bank
from app.security import get_current_user
from app import schemas, models

router = APIRouter(prefix="/bank", tags=["bank"])

@router.post("/link", response_model=schemas.BankAccountOut)
def link_bank(payload: schemas.BankLinkIn, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    info = mock_bank.create_link(cast(int, current_user.id), payload.provider or "mock", payload.last_four or "0000")
    acct = models.BankAccount(user_id=cast(int, current_user.id), provider=info["provider"], external_id=None, last_four=info["last_four"])
    db.add(acct)
    db.commit()
    db.refresh(acct)
    return acct

@router.get("/account", response_model=schemas.BankAccountOut)
def get_account(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    acct = db.query(models.BankAccount).filter(models.BankAccount.user_id == cast(int, current_user.id)).first()
    if not acct:
        raise HTTPException(status_code=404, detail="No linked bank account")
    return acct