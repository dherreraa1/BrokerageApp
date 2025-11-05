from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Auth
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Trading
class TradeCreate(BaseModel):
    symbol: str
    side: str  # 'buy' or 'sell'
    quantity: float
    price: float

class TradeOut(BaseModel):
    id: int
    symbol: str
    side: str
    quantity: float
    price: float
    executed_value: float
    executed_at: datetime

    class Config:
        from_attributes = True

# Bank
class BankLinkIn(BaseModel):
    provider: Optional[str] = None
    last_four: Optional[str] = None

class BankAccountOut(BaseModel):
    id: int
    provider: Optional[str]
    last_four: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Portfolio
class Holding(BaseModel):
    symbol: str
    quantity: float
    avg_price: float

class PortfolioOut(BaseModel):
    balance: float
    holdings: List[Holding] = []
