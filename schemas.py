from pydantic import BaseModel

class UtilizatorCreate(BaseModel):
    email: str
    parola: str

class SarcinaCreate(BaseModel):
    titlu: str
    descriere: str | None = None

class SarcinaUpdate(BaseModel):
    titlu: str | None = None
    descriere: str | None = None

class SarcinaOut(BaseModel):
    id: int
    titlu: str
    descriere: str | None
    finalizata: bool

    class Config:
        from_attributes = True