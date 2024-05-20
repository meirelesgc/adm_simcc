from pydantic import BaseModel


class ResearcherGroup(BaseModel):
    nome_grupo: str
    nome_lider: str
    area: str
    ultimo_envio: str
    situacao: str
    instituicao: str


class ListResearcherGroup(BaseModel):
    researcher_groups_list: list[ResearcherGroup]
