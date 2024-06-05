import os
from ..dao import Connection
from pydantic import UUID4

adm_database = Connection()


def request_load(institution_id: UUID4):
    script_sql = f"""
        UPDATE institution
        SET load_status = 'CARGA SOLICITADA'
        WHERE institution_id = '{institution_id}'
        """
    adm_database.exec(script_sql)


def check_load():
    with open(os.environ["HOP_LOG_PATH"], "r", encoding="utf-8") as archive:
        lines = archive.readlines()
        for line in reversed(lines):
            stripped_line = line.strip()
            if stripped_line:
                return stripped_line
        return None
