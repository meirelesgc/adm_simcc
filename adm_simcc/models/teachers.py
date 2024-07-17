from pydantic import BaseModel, field_validator
from datetime import datetime


class Teacher(BaseModel):
    matric: int
    inscUFMG: int
    nome: str
    genero: str
    situacao: str
    rt: str
    clas: int
    cargo: str
    classe: str
    ref: int
    titulacao: str
    entradaNaUFMG: datetime
    progressao: datetime
    year_charge: int
    semester: int

    @field_validator("entradaNaUFMG", mode="before")
    def parse_entradaNaUFMG(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")

    @field_validator("progressao", mode="before")
    def parse_progressao(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")


class ListTeachers(BaseModel):
    list_teachers: list[Teacher]
