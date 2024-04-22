class GraduateProgramResearcher(object):
    def __init__(self):
        self.name = None
        self.lattes_id = None
        self.type_ = ""

    def get_json(self):
        graduate_program_researcher = {
            "name": str(self.name),
            "lattes_id": str(self.lattes_id),
            "type_": str(self.type_),
        }
        return graduate_program_researcher
