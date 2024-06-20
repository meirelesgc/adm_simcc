from dataclasses import dataclass, asdict
from uuid import uuid4


@dataclass
class Institution:
    institution_id: uuid4
    name: str
    acronym: str
    lattes_id: str

    def get_json(self):
        return asdict(self)


@dataclass
class ListInstitutions:
    institution_list: list[Institution]

    def add_institution(self, institution: Institution):
        self.institutions.append(institution)

    def get_json(self):
        return [inst.get_json() for inst in self.institutions]
