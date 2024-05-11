from pydantic import UUID4, BaseModel


class ResearcherGroup(BaseModel):
    research_group_id: UUID4
    research_group_name: str
    researcher_id: UUID4
    leader_name: str
    institution_id: UUID4
    institution_name: str
    acronym: str
    area: str
    last_date_sent: str
    situation: str
    lattes_id: int
    file_path: str
