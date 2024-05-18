from pydantic import BaseModel, Field, AliasChoices
from pydantic_br import CPF


class ResearcherGroup(BaseModel):
    nome_grupo: str
    nome_lider: str
    cpf: CPF
    area: str
    ultimo_envio: str
    situacao: str
    instituicao: str


class ListResearcherGroup(BaseModel):
    researcher_groups_list: list[ResearcherGroup]
