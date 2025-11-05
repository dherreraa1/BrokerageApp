from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, bank, trading, portfolio

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brokerage App - Part I")

app.include_router(auth.router)
app.include_router(bank.router)
app.include_router(trading.router)
app.include_router(portfolio.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Brokerage App running"}
