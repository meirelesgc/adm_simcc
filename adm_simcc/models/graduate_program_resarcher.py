from typing import List
from pydantic import UUID4, BaseModel, validator
from typing import Optional


class GraduateProgramResearcher(BaseModel):
    graduate_program_id: UUID4
    researcher_id: Optional[UUID4] = None
    year: list
    type_: str
    lattes_id: Optional[str]

    @validator('year', pre=True)
    def split_year(cls, v):
        return [int(year.strip()) for year in v.split(';')]


class ListResearcher(BaseModel):
    researcher_list: list[GraduateProgramResearcher]
