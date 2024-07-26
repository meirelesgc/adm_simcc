from pydantic import BaseModel, field_validator
from datetime import datetime


class Technician(BaseModel):
    matric: str
    insUFMG: str
    nome: str
    genero: str
    denoSit: str
    rt: str
    classe: str
    cargo: str
    nivel: str
    ref: str
    titulacao: str
    setor: str
    detalheSetor: str
    dtYngOrg: datetime
    dataProg: datetime
    year_charge: str
    semester: str

    @field_validator("dting_org", mode="before")
    def parse_dting_org(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")

    @field_validator("data_prog", mode="before")
    def parse_data_prog(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")


class ListTechnician(BaseModel):
    list_technician: list[Technician]
