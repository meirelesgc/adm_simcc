from typing import Optional

from pydantic import UUID4, BaseModel


class GraduateProgramResearcher(BaseModel):
    graduate_program_id: UUID4
    researcher_id: UUID4
    year: Optional[int]
    type_: str


class ListResearcher(BaseModel):
    researcher_list: list[GraduateProgramResearcher]
