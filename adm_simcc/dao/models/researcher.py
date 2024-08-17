from pydantic import UUID4, BaseModel


class Researcher(BaseModel):
    researcher_id: UUID4
    name: str
    lattes_id: str
    institution_id: UUID4


class ListResearchers(BaseModel):
    researcher_list: list[Researcher]


class Subsidies(BaseModel):
    id: int
    id_lattes: str
    nome_beneficiario: str
    cpf_beneficiario: str
    nome_pais: str
    nome_regiao: str
    nome_uf: str
    nome_cidade: str
    nome_grande_area: str
    nome_area: str
    nome_sub_area: str
    cod_modalidade: str
    nome_modalidade: str
    titulo_chamada: str
    cod_categoria_nivel: str
    nome_programa_fomento: str
    nome_instituto: str
    quant_auxilio: str
    quant_bolsa: int


class ListSubsidies(BaseModel):
    grant_list: list[Subsidies]


class ResearcherDepartament(BaseModel):
    dep_id: int
    researcher_id: UUID4


class ListResearcherDepartament(BaseModel):
    researcher_departament: list[ResearcherDepartament]
