from pydantic import UUID4, BaseModel


class Institution(BaseModel):
    institution_id: UUID4
    name: str
    acronym: str
    lattes_id: int
