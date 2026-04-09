# // (c) 2026 Guillermo Roger Hernandez Chandia - ADS
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Response, Depends, HTTPException, Header, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pandas as pd
import io

load_dotenv()
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

# Configuração para aparecer o cadeado no Swagger
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def verify_key(x_api_key: str = Security(api_key_header)):
    if not API_SECRET_KEY or x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Acesso Proibido: Sistema Protegido")
    return x_api_key

DATABASE_URL = "sqlite:///./fraud_logs.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBAnalysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    amount = Column(Float)
    score = Column(Float)
    risk_level = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Título personalizado para o seu Tesouro
app = FastAPI(title="FraudShield API - Guillermo ADS", version="5.2")

class Transaction(BaseModel):
    user_id: int
    amount: float
    location: str
    is_new_device: bool

@app.post('/analyze', dependencies=[Depends(verify_key)])
def analyze(trx: Transaction):
    db = SessionLocal()
    one_min_ago = datetime.utcnow() - timedelta(minutes=1)
    recent_txs = db.query(DBAnalysis).filter(DBAnalysis.user_id == trx.user_id, DBAnalysis.timestamp >= one_min_ago).count()
    
    score = min(100, trx.amount / 100)
    if trx.is_new_device: score += 20
    if recent_txs >= 3: score = 100
    
    score = min(100, score)
    risk = "high" if score >= 80 else "medium" if score >= 40 else "low"
    
    new_log = DBAnalysis(user_id=trx.user_id, amount=trx.amount, score=score, risk_level=risk)
    db.add(new_log)
    db.commit()
    db.close()
    return {"score": round(score, 2), "risk_level": risk, "status": "Protected by Guillermo"}

@app.get('/export-csv', dependencies=[Depends(verify_key)])
def export_csv():
    db = SessionLocal()
    logs = db.query(DBAnalysis).all()
    db.close()
    df = pd.DataFrame([{"user": l.user_id, "amount": l.amount, "score": l.score, "risk": l.risk_level} for l in logs])
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    return Response(content=stream.getvalue(), media_type="text/csv")
