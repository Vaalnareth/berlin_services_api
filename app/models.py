from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy import Column, Text

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    voraussetzungen: Optional[str] = Field(sa_column=Column(Text))
    erforderliche_unterlagen: Optional[str] = Field(sa_column=Column(Text))
    gebuehren: Optional[str] = Field(sa_column=Column(Text))
    rechtsgrundlagen: Optional[str] = Field(sa_column=Column(Text))
    digital_service: bool
    zustaendiges_amt: Optional[str] = Field(sa_column=Column(Text))
    forms: List["Form"] = Relationship(back_populates="service")

class Form(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str
    service_id: Optional[int] = Field(default=None, foreign_key="service.id")
    service: Optional[Service] = Relationship(back_populates="forms")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_active: bool = Field(default=True)