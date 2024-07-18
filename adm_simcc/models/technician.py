from pydantic import BaseModel, field_validator
from datetime import datetime


class Technician(BaseModel):
    matric: int
    ins_ufmg: int
    nome: str
    genero: str
    deno_sit: str
    rt: str
    classe: str
    cargo: str
    nivel: str
    ref: str
    titulacao: str
    setor: str
    detalhe_setor: str
    dting_org: datetime
    data_prog: datetime
    year_charge: int
    semester: int

    @field_validator("dting_org", mode="before")
    def parse_dting_org(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")

    @field_validator("data_prog", mode="before")
    def parse_data_prog(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")


class ListTechnician(BaseModel):
    list_technician: list[Technician]
