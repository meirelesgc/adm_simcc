from typing import Optional
from pydantic import UUID4, BaseModel, model_validator


class GraduateProgram(BaseModel):
    graduate_program_id: UUID4
    code: Optional[str]
    name: str
    area: str
    modality: str
    type: Optional[str]
    rating: Optional[str]
    institution_id: UUID4
    state: str = "BA"
    city: str = "Salvador"
    region: str = "Nordeste"
    instituicao: Optional[str]
    url_image: Optional[str]
    sigla: Optional[str]
    description: Optional[str]
    visible: bool = False


class ListGraduateProgram(BaseModel):
    graduate_program_list: list[GraduateProgram]
