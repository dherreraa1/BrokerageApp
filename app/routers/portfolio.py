from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import cast, Dict
from app.dependencies import get_db
from app.security import get_current_user
from app import models
from app import schemas

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("/", response_model=schemas.PortfolioOut)
def get_portfolio(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    trades = db.query(models.Trade).filter(models.Trade.user_id == cast(int, current_user.id)).all()
    holdings: Dict[str, float] = {}
    cost_basis: Dict[str, float] = {}
    for t in trades:
        qty = cast(float, t.quantity) if cast(str, t.side).lower() == "buy" else -cast(float, t.quantity)
        holdings[cast(str, t.symbol)] = holdings.get(cast(str, t.symbol), 0.0) + qty
        cost_basis[cast(str, t.symbol)] = cost_basis.get(cast(str, t.symbol), 0.0) + (cast(float, t.price) * (cast(float, t.quantity) if cast(str, t.side).lower() == "buy" else -cast(float, t.quantity)))
    holding_list = []
    for sym, qty in holdings.items():
        if abs(qty) < 1e-9:
            continue
        avg_price = abs(cost_basis.get(sym, 0.0) / qty) if qty != 0 else 0.0
        holding_list.append(schemas.Holding(symbol=sym, quantity=qty, avg_price=round(avg_price, 8)))
    return schemas.PortfolioOut(balance=cast(float, current_user.balance), holdings=holding_list)