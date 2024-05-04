class ResearchGroup(object):
    def __init__(self):
        self.research_group_id = None
        self.research_group_name = ""
        self.researcher_id = ""
        self.leader_name = ""
        self.institution_id = ""
        self.institution_name = ""
        self.acronym = ""
        self.area = ""
        self.last_date_sent = ""
        self.situation = ""
        self.lattes_id = ""
        self.file_path = ""

    def get_json(self):
        research_group = {
            "research_group_id": str(self.research_group_id),
            "research_group_name": str(self.research_group_name),
            "researcher_id": str(self.researcher_id),
            "leader_name": str(self.leader_name),
            "institution_id": str(self.institution_id),
            "institution_name": str(self.institution_name),
            "acronym": str(self.acronym),
            "area": str(self.area),
            "last_date_sent": str(self.last_date_sent),
            "situation": str(self.situation),
            "lattes_id": str(self.lattes_id),
        }

        return research_group