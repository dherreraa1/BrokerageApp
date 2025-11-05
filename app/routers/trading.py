from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import cast
from app.dependencies import get_db
from app.utils.exchange_adapter import exchange
from app.security import get_current_user
from app import schemas, models
from datetime import datetime, timezone

router = APIRouter(prefix="/trading", tags=["trading"])

@router.get("/instruments")
def instruments():
    return exchange.list_instruments()

@router.post("/execute", response_model=schemas.TradeOut)
def execute_trade(payload: schemas.TradeCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    price = exchange.get_price(payload.symbol)
    if price is None:
        raise HTTPException(status_code=404, detail="Instrument not found")

    cost = payload.price * payload.quantity
    if payload.side.lower() == "buy":
        if cast(float, current_user.balance) < cost:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
        current_user.balance = cast(float, current_user.balance) - cost # type: ignore
    elif payload.side.lower() == "sell":
        current_user.balance = cast(float, current_user.balance) + cost # type: ignore
    else:
        raise HTTPException(status_code=400, detail="Invalid side")

    # Execute
    exec_result = exchange.execute_trade(cast(int, current_user.id), payload)

    # Persist trade and user balance
    executed_at = datetime.fromisoformat(exec_result["executed_at"]) if isinstance(exec_result["executed_at"], str) else datetime.now(timezone.utc)
    trade = models.Trade(
        user_id=cast(int, current_user.id),
        symbol=exec_result["symbol"],
        side=exec_result["side"],
        quantity=exec_result["quantity"],
        price=exec_result["price"],
        executed_value=exec_result["executed_value"],
        executed_at=executed_at,
        trade_metadata=str(exec_result)
    )
    db.add(trade)
    db.add(current_user)
    db.commit()
    db.refresh(trade)
    db.refresh(current_user)

    return schemas.TradeOut(
        id=cast(int, trade.id),
        symbol=cast(str, trade.symbol),
        side=cast(str, trade.side),
        quantity=cast(float, trade.quantity),
        price=cast(float, trade.price),
        executed_value=cast(float, trade.executed_value),
        executed_at=cast(datetime, trade.executed_at)
    )