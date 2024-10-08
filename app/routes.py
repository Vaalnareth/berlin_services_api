from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_session
from app.models import Service, Form, User
from app.auth import authenticate_user, create_access_token, get_current_active_user
from typing import Optional, List

router = APIRouter()

@router.post("/token", response_model=dict)
def login_for_access_token(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/services/")
def read_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    services = db.query(Service).offset(skip).limit(limit).all()
    return services

@router.get("/ALL-SERVICES")
def get_all_services(
    digital_service: Optional[bool] = Query(None, alias="DIGITAL-SERVICE"),
    responsible_office: Optional[str] = Query(None, alias="RESPONSIBLE-OFFICE"),
    db: Session = Depends(get_session)
):
    query = db.query(Service)
    
    if digital_service is not None:
        query = query.filter(Service.digital_service == digital_service)
    
    if responsible_office:
        query = query.filter(Service.zustaendiges_amt == responsible_office)
    
    services = query.all()
    return services

@router.get("/ALL-SERVICES", response_model=List[dict])
def get_all_service_titles(db: Session = Depends(get_session)):
    services = db.query(Service).all()
    return [{"id": service.id, "title": service.title} for service in services]

@router.get("/SERVICE/{service_id}", response_model=Service)
def get_service(service_id: int, db: Session = Depends(get_session)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.get("/ALL-FORMS", response_model=List[dict])
def get_all_forms(db: Session = Depends(get_session)):
    forms = db.query(Form).all()
    return [{"id": form.id, "title": form.title, "url": form.url} for form in forms]