from fastapi import FastAPI, Query
from typing import List
from sqlalchemy import create_engine, text
from datetime import datetime
import os

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db_fonte:5432/fonte")
engine = create_engine(DATABASE_URL)

@app.get("/data/")
def get_data(inicio: datetime, fim: datetime, colunas: List[str] = Query(["wind_speed"])):	
    
    colunas_retorno = ', '.join(["timestamp"] + colunas)
    
    query = text(f"""
    SELECT {colunas_retorno} 
    FROM data 
    WHERE timestamp BETWEEN :inicio AND :fim
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, parameters={"inicio": inicio, "fim": fim})
        rows = [dict(row._mapping) for row in result]

    return rows