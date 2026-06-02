from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas, auth
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="autentificare")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        return db.query(models.Utilizator).filter_by(email=email).first()
    except:
        raise HTTPException(status_code=401)

@app.post("/inregistrare")
def register(user: schemas.UtilizatorCreate, db: Session = Depends(get_db)):
    if db.query(models.Utilizator).filter_by(email=user.email).first():
        raise HTTPException(400, "Email existent")

    u = models.Utilizator(
        email=user.email,
        parola_hash=auth.hash_parola(user.parola)
    )
    db.add(u)
    db.commit()
    return {"msg": "ok"}

@app.post("/autentificare")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Utilizator).filter_by(email=form.username).first()

    if not user or not auth.verifica_parola(form.password, user.parola_hash):
        raise HTTPException(400, "Date greșite")

    token = auth.creeaza_token({"sub": user.email})
    return {"access_token": token}

@app.post("/sarcini")
def create_task(task: schemas.SarcinaCreate, db: Session = Depends(get_db), user=Depends(get_user)):
    t = models.Sarcina(**task.dict(), utilizator_id=user.id)
    db.add(t)
    db.commit()
    return t

@app.get("/sarcini")
def get_tasks(doar_nefinalizate: bool = False, db: Session = Depends(get_db), user=Depends(get_user)):
    q = db.query(models.Sarcina).filter_by(utilizator_id=user.id)

    if doar_nefinalizate:
        q = q.filter_by(finalizata=False)

    return q.all()

@app.put("/sarcini/{id}")
def update_task(id: int, data: schemas.SarcinaUpdate, db: Session = Depends(get_db), user=Depends(get_user)):
    task = db.query(models.Sarcina).filter_by(id=id, utilizator_id=user.id).first()

    if not task:
        raise HTTPException(404)

    if data.titlu is not None:
        task.titlu = data.titlu
    if data.descriere is not None:
        task.descriere = data.descriere

    db.commit()
    return task

@app.patch("/sarcini/{id}/finaliza")
def finalize(id: int, db: Session = Depends(get_db), user=Depends(get_user)):
    task = db.query(models.Sarcina).filter_by(id=id, utilizator_id=user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task inexistent")

    task.finalizata = True
    db.commit()
    return {"msg": "ok"}

@app.delete("/sarcini/{id}")
def delete(id: int, db: Session = Depends(get_db), user=Depends(get_user)):
    task = db.query(models.Sarcina).filter_by(id=id, utilizator_id=user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task inexistent")

    db.delete(task)
    db.commit()
    return {"msg": "sters"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")