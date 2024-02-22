class Institution(object):
    def __init__(self):
        self.institution_id = None
        self.name = ""
        self.acronym = ""
        self.lattes_id = ""

    def get_json(self):
        institution = {
            "institution_id": str(self.institution_id),
            "name": str(self.name),
            "acronym": str(self.acronym),
            "lattes_id": str(self.lattes_id),
        }

        return institution
