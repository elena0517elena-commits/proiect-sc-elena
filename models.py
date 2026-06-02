from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Utilizator(Base):
    __tablename__ = "utilizatori"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    parola_hash = Column(String)

class Sarcina(Base):
    __tablename__ = "sarcini"

    id = Column(Integer, primary_key=True, index=True)
    titlu = Column(String)
    descriere = Column(String, nullable=True)
    finalizata = Column(Boolean, default=False)
    utilizator_id = Column(Integer, ForeignKey("utilizatori.id"))