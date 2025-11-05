from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

def now_utc():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  
    hashed_password = Column(String, nullable=False)  
    balance = Column(Float, default=10000.0)
    created_at = Column(DateTime, default=now_utc)

    bank_accounts = relationship("BankAccount", back_populates="owner")
    trades = relationship("Trade", back_populates="owner")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=True)
    external_id = Column(String, nullable=True)
    last_four = Column(String(4), nullable=True)
    created_at = Column(DateTime, default=now_utc)

    owner = relationship("User", back_populates="bank_accounts")

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy / sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    executed_value = Column(Float, nullable=False)
    executed_at = Column(DateTime, default=now_utc)
    trade_metadata = Column(Text, nullable=True)

    owner = relationship("User", back_populates="trades")
