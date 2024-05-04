import pandas as pd
from Dao.dbHandler import db_script, db_select
from Model.ResearchGroup import ResearchGroup


def Insert(research_group):
    sql = f"""
        INSERT INTO research_group (
            research_group_name, researcher_id, institution_id,
            area, last_date_sent, situation, file_path
        ) VALUES (
            {f"'{research_group.research_group_name}'" if research_group.research_group_name else 'NULL'},
            {f"'{research_group.researcher_id}'" if research_group.researcher_id else 'NULL'},
            {f"'{research_group.institution_id}'" if research_group.institution_id else 'NULL'},
            {f"'{research_group.area}'" if research_group.area else 'NULL'},
            {f"'{research_group.last_date_sent}'" if research_group.last_date_sent else 'NULL'},
            {f"'{research_group.situation}'" if research_group.situation else 'NULL'},
            {f"'{research_group.file_path}'" if research_group.file_path else 'NULL'}
        )
    """

    return db_script(sql)

def Query():
    sql = """
        SELECT 
            rg.research_group_id, 
            rg.research_group_name, 
            rg.area, 
            rg.last_date_sent, 
            rg.situation,
            r.researcher_id,
            r.name AS leader_name,
            r.lattes_id,
            i.institution_id,
            i.name AS institution_name,
            i.acronym
        FROM research_group AS rg
        LEFT JOIN researcher AS r
        ON r.researcher_id = rg.researcher_id
        LEFT JOIN institution AS i
        ON rg.institution_id = i.institution_id;
        """

    return pd.DataFrame(
        db_select(sql),
        columns=[
            "research_group_id",
            "research_group_name",
            "area",
            "last_date_sent",
            "situation",
            "researcher_id",
            "leader_name",
            "lattes_id",
            "institution_id",
            "institution_name",
            "acronym",
        ],
    ) 

def QueryById(research_group_id):
    sql = f"""
        SELECT 
            rg.research_group_id, 
            rg.research_group_name, 
            rg.area, 
            rg.last_date_sent, 
            rg.situation,
            r.researcher_id,
            r.name AS leader_name,
            r.lattes_id,
            i.institution_id,
            i.name AS institution_name,
            i.acronym
        FROM research_group AS rg
        LEFT JOIN researcher AS r
        ON r.researcher_id = rg.researcher_id
        LEFT JOIN institution AS i
        ON rg.institution_id = i.institution_id
        WHERE 
            rg.research_group_id = '{research_group_id}'
        """

    return pd.DataFrame(
        db_select(sql),
        columns=[
            "research_group_id",
            "research_group_name",
            "area",
            "last_date_sent",
            "situation",
            "researcher_id",
            "leader_name",
            "lattes_id",
            "institution_id",
            "institution_name",
            "acronym",
        ],
    )


def QueryByReseacherId(researcher_id):
    sql = f"""
        SELECT 
            rg.research_group_id, 
            rg.research_group_name, 
            rg.area, 
            rg.last_date_sent, 
            rg.situation,
            r.researcher_id,
            r.name AS leader_name,
            r.lattes_id,
            i.institution_id,
            i.name AS institution_name,
            i.acronym
        FROM research_group AS rg
        LEFT JOIN researcher AS r
        ON r.researcher_id = rg.researcher_id
        LEFT JOIN institution AS i
        ON rg.institution_id = i.institution_id
        WHERE 
            r.researcher_id = '{researcher_id}'
        """

    return pd.DataFrame(
        db_select(sql),
        columns=[
            "research_group_id",
            "research_group_name",
            "area",
            "last_date_sent",
            "situation",
            "researcher_id",
            "leader_name",
            "lattes_id",
            "institution_id",
            "institution_name",
            "acronym",
        ],
    )



def QueryByInstitutionId(institution_id):
    sql = f"""
        SELECT 
            rg.research_group_id, 
            rg.research_group_name, 
            rg.area, 
            rg.last_date_sent, 
            rg.situation,
            r.researcher_id,
            r.name AS leader_name,
            r.lattes_id,
            i.institution_id,
            i.name AS institution_name,
            i.acronym
        FROM research_group AS rg
        LEFT JOIN researcher AS r
        ON r.researcher_id = rg.researcher_id
        LEFT JOIN institution AS i
        ON rg.institution_id = i.institution_id
        WHERE 
            i.institution_id = '{institution_id}'
        """

    return pd.DataFrame(
        db_select(sql),
        columns=[
            "research_group_id",
            "research_group_name",
            "area",
            "last_date_sent",
            "situation",
            "researcher_id",
            "leader_name",
            "lattes_id",
            "institution_id",
            "institution_name",
            "acronym",
        ],
    )


def Delete(research_group_id):
    sql = """
    DELETE FROM research_group WHERE research_group_id = '{filter}';
""".format(
        filter=research_group_id
    )
    db_script(sql)
    return "OK"


def DeleteByInstitutionId(institution_id):
    sql = """
    DELETE FROM research_group WHERE institution_id = '{filter}';
""".format(
        filter=institution_id
    )
    db_script(sql)
    return "OK"