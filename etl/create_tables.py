from sqlalchemy import create_engine
from models import Base

# script para criar as tabelas no banco de dados alvo
DATABASE_URL_ALVO = "postgresql://user:password@db_alvo:5432/alvo"
engine = create_engine(DATABASE_URL_ALVO)

Base.metadata.create_all(engine)