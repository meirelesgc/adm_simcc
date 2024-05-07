class GraduateProgramResearcher(object):
    def __init__(self):
        self.graduate_program_id = str
        self.lattes_id = int
        self.year = str
        self.type_ = ""

    def get_json(self):
        graduate_program_researcher = {
            "graduate_program_id": str(self.name),
            "lattes_id": str(self.lattes_id),
            "year": str(self.year),
            "type_": str(self.type_),
        }
        return graduate_program_researcher
