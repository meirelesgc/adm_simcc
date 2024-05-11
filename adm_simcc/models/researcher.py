from pydantic import UUID4, BaseModel


class Researcher(BaseModel):
    researcher_id: UUID4
    name: str
    lattes_id: int
    institution_id: UUID4
