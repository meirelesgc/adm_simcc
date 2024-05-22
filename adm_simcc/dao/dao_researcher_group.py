import pandas as pd
from ..dao import Connection, dao_researcher
from ..models.researcher_group import ListResearcherGroup

adm_database = Connection()


def research_group_insert(ListResearcherGroup: ListResearcherGroup):
    values = str()

    for research_group in ListResearcherGroup.researcher_groups_list:
        researcher_name = research_group.nome_lider
        researcher_id = dao_researcher.researcher_query_name(researcher_name)

        values += f"""(
            {f"'{research_group.nome_grupo}'" if research_group.nome_grupo else 'NULL'},
            {f"'{researcher_id}'" if researcher_id else 'NULL'},
            {f"'{research_group.institution_id}'"},
            {f"'{research_group.area}'" if research_group.area else 'NULL'},
            {f"'{research_group.ultimo_envio}'" if research_group.ultimo_envio else 'NULL'},
            {f"'{research_group.situacao}'" if research_group.situacao else 'NULL'}),"""

    script_sql = f"""
        INSERT INTO research_group 
        (research_group_name, researcher_id, institution_id, area, 
        last_date_sent, situation) 
        VALUES {values[:-1]}
    """

    adm_database.exec(script_sql)


def research_group_basic_query(institution_id, research_group_id, researcher_id):
    filter_institution = str()
    filter_research_group = str()
    filter_researcher = str()

    if institution_id:
        filter_institution = f"AND i.institution_id = '{institution_id}'"
    if research_group_id:
        filter_research_group = f"AND rg.research_group_id = '{research_group_id}'"
    if researcher_id:
        filter_researcher = f"AND r.researcher_id = '{researcher_id}'"

    script_sql = f"""
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
            rg.institution_id IS NOT NULL
            {filter_institution}
            {filter_research_group}
            {filter_researcher}
        """
    registry = adm_database.select(script_sql)
    data_frame = pd.DataFrame(
        registry,
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

    return data_frame.to_dict(orient="records")


def research_group_delete(research_group_id: str = None, institution_id: str = None):
    if research_group_id:
        script_sql = f"""
            DELETE FROM research_group WHERE research_group_id = '{research_group_id}';
            """
    if institution_id:
        script_sql = f"""
            DELETE FROM research_group WHERE institution_id = '{institution_id}';
            """

    adm_database.exec(script_sql)
