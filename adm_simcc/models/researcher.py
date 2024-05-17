from pydantic import UUID4, BaseModel, Field


class Researcher(BaseModel):
    researcher_id: UUID4
    name: str
    lattes_id: str
    institution_id: UUID4


class ListResearchers(BaseModel):
    researcher_list: list[Researcher]
