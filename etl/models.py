from sqlalchemy import Column, Integer, String, Date, Time, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# estabelece o padrão da tabela alvo

class Signal(Base):
    __tablename__ = 'signal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    timestamp = Column(Time, nullable=False)
    signal_id = Column(Integer, nullable=True)
    value = Column(Float, nullable=False)


