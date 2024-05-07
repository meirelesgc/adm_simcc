import pandas as pd
from numpy import NaN

import Dao.dbHandler as dbHandler
from Dao import sgbdSQL


def article_prod(Data):

    script_sql = f"""
        SELECT
            bp.year,
            qualis,
            COUNT(DISTINCT title) AS count_article
        FROM
            public.bibliographic_production bp
        JOIN
            public.bibliographic_production_article bpa ON
            bp.id = bpa.bibliographic_production_id
        JOIN
            public.graduate_program_researcher gpr ON
            gpr.researcher_id = bp.researcher_id
        WHERE
            type = 'ARTICLE'
            AND gpr.graduate_program_id = '{Data['graduate_program_id']}'
        GROUP BY
            bp.year, qualis
        ORDER BY
            bp.year, qualis;
        """
    registry = sgbdSQL.consultar_db(script_sql)

    df_ind_prod_base_article = pd.DataFrame(
        registry, columns=["year", "qualis", "count_article"]
    )
    df_ind_prod_base_article["ind_prod_article"] = (
        df_ind_prod_base_article["qualis"].map(weights)
        * df_ind_prod_base_article["count_article"]
    )

    df_ind_prod_base_article = df_ind_prod_base_article.groupby("year", as_index=False)[
        "ind_prod_article"
    ].sum()

    df_ind_prod_base_article["year"] = df_ind_prod_base_article["year"].astype(int)
    return df_ind_prod_base_article


def book_prod(Data):
    script_sql = f"""
        SELECT
            bp.year,
            COUNT(DISTINCT title) AS count_book
        FROM
            public.bibliographic_production bp
        JOIN graduate_program_researcher gpr ON
            gpr.researcher_id = bp.researcher_id
        WHERE
            type = 'BOOK'
            AND gpr.graduate_program_id = '{Data['graduate_program_id']}'
        GROUP BY
            bp.year
        ORDER BY
            bp.year;
                """

    registry = sgbdSQL.consultar_db(script_sql)

    df_ind_prod_base_book = pd.DataFrame(registry, columns=["year", "count_book"])

    df_ind_prod_base_book["ind_prod_book"] = (
        df_ind_prod_base_book["count_book"] * weights["BOOK"]
    )
    df_ind_prod_base_book = df_ind_prod_base_book.drop("count_book", axis=1)
    df_ind_prod_base_book["year"] = df_ind_prod_base_book["year"].astype(int)
    return df_ind_prod_base_book


def book_chapter_prod(Data):

    script_sql = f"""
        SELECT
            bp.year,
            COUNT(DISTINCT title) AS count_book_chapter
        FROM
            public.bibliographic_production bp
        JOIN
            public.graduate_program_researcher gpr ON
            gpr.researcher_id = bp.researcher_id
        WHERE
            type = 'BOOK_CHAPTER'
            AND gpr.graduate_program_id = '{Data['graduate_program_id']}'
        GROUP BY
            bp.year
        ORDER BY
            bp.year;
        """

    registry = sgbdSQL.consultar_db(script_sql)

    df_ind_prod_base_book_chapter = pd.DataFrame(
        registry, columns=["year", "count_book_chapter"]
    )

    df_ind_prod_base_book_chapter["ind_prod_book_chapter"] = (
        df_ind_prod_base_book_chapter["count_book_chapter"] * weights["BOOK_CHAPTER"]
    )
    df_ind_prod_base_book_chapter = df_ind_prod_base_book_chapter.drop(
        "count_book_chapter", axis=1
    )
    df_ind_prod_base_book_chapter["year"] = df_ind_prod_base_book_chapter[
        "year"
    ].astype(int)
    return df_ind_prod_base_book_chapter


def patent_prod(Data):
    script_sql = f"""
        SELECT
            development_year,
            'PATENT_GRANTED' as granted,
            COUNT(DISTINCT title) as count_patent
        FROM 
            patent p
        JOIN public.graduate_program_researcher gpr ON
            gpr.researcher_id = p.researcher_id
        WHERE
            gpr.graduate_program_id = '{Data['graduate_program_id']}'
            AND grant_date IS NOT NULL
        GROUP BY 
            development_year

        UNION

        SELECT
            development_year,
            'PATENT_NOT_GRANTED',
            COUNT(DISTINCT title) as count_patent
        FROM 
            patent p
        JOIN public.graduate_program_researcher gpr ON
            gpr.researcher_id = p.researcher_id
        WHERE
            gpr.graduate_program_id = '{Data['graduate_program_id']}'
            AND grant_date IS NULL
        GROUP BY 
            development_year
        """
    registry = sgbdSQL.consultar_db(script_sql)

    df_ind_prod_base_patent = pd.DataFrame(
        registry, columns=["year", "granted", "count_patent"]
    )

    df_ind_prod_base_patent["ind_prod_patent"] = (
        df_ind_prod_base_patent["granted"].map(weights)
        * df_ind_prod_base_patent["count_patent"]
    )
    df_ind_prod_base_patent = df_ind_prod_base_patent.pivot(
        index="year", columns="granted", values="ind_prod_patent"
    )
    df_ind_prod_base_patent = df_ind_prod_base_patent.rename(
        columns={
            "PATENT_GRANTED": "ind_prod_granted_patent",
            "PATENT_NOT_GRANTED": "ind_prod_not_granted_patent",
        }
    )
    df_ind_prod_base_patent = df_ind_prod_base_patent.reset_index()
    df_ind_prod_base_patent["year"] = df_ind_prod_base_patent["year"].astype(int)

    return df_ind_prod_base_patent


def software_prod(Data):
    script_sql = f"""
        SELECT
            sw.year,
            COUNT(DISTINCT title) as count_software
        FROM 
            public.software sw
        JOIN public.graduate_program_researcher gpr ON
            gpr.researcher_id = sw.researcher_id
        WHERE
            gpr.graduate_program_id = '{Data['graduate_program_id']}'
        GROUP BY
            sw.year
        """

    registry = sgbdSQL.consultar_db(script_sql)

    df_ind_prod_base_software = pd.DataFrame(
        registry, columns=["year", "count_software"]
    )

    df_ind_prod_base_software["ind_prod_software"] = (
        df_ind_prod_base_software["count_software"] * weights["SOFTWARE"]
    )
    df_ind_prod_base_software["year"] = df_ind_prod_base_software["year"].astype(int)
    return df_ind_prod_base_software


def report_prod(Data):
    script_sql = f"""
        SELECT
            rr.year,
            COUNT(DISTINCT title) as count_report
        FROM 
            research_report rr
        JOIN graduate_program_researcher gp ON
            gp.researcher_id = rr.researcher_id 
        WHERE 
            gp.graduate_program_id = '{Data['graduate_program_id']}'
        GROUP BY
            rr.year
        ORDER BY 
            rr.year
        """

    registry = sgbdSQL.consultar_db(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=["year", "count_report"],
    )

    data_frame["ind_prod_report"] = data_frame["count_report"] * weights["REPORT"]

    return data_frame


def calc_ind_prod(weights):

    year = list(range(2008, 2025))

    script_sql = """
        SELECT 
            graduate_program_id, 
            name 
        FROM 
            graduate_program
        """

    registry = sgbdSQL.consultar_db(script_sql)

    df_graduate_program = pd.DataFrame(
        registry, columns=["graduate_program_id", "name"]
    )

    for Index, Data in df_graduate_program.iterrows():

        data_frame = pd.DataFrame(year, columns=["year"])

        df = article_prod(Data=Data)

        if not df.empty:
            data_frame = pd.merge(data_frame, df, on="year", how="left")
        else:
            data_frame["ind_prod_article"] = NaN

        df = book_prod(Data=Data)

        if not df.empty:
            data_frame = pd.merge(data_frame, df, on="year", how="left")
        else:
            data_frame["ind_prod_book"] = NaN

        df = book_chapter_prod(Data=Data)

        if not df.empty:
            data_frame = pd.merge(data_frame, df, on="year", how="left")
        else:
            data_frame["ind_prod_book_chapter"] = NaN

        df = patent_prod(Data=Data)
        if not df.empty:
            data_frame = pd.merge(data_frame, df, on="year", how="left")
        if "ind_prod_granted_patent" not in df.columns:
            data_frame["ind_prod_granted_patent"] = NaN
        if "ind_prod_not_granted_patent" not in df.columns:
            data_frame["ind_prod_not_granted_patent"] = NaN

        df = software_prod(Data=Data)
        if not df.empty:
            data_frame = pd.merge(data_frame, df, on="year", how="left")
        else:
            data_frame["ind_prod_software"] = NaN

        df = report_prod(Data=Data)

        if not df.empty:
            data_frame = pd.merge(data_frame, df, on="year", how="left")
        else:
            data_frame["ind_prod_report"] = NaN

        for Intern_Index, Intern_Data in data_frame.fillna(0).iterrows():
            script_sql = f"""
            INSERT INTO public.graduate_program_ind_prod(
                graduate_program_id,
                year,
                ind_prod_article,
                ind_prod_book,
                ind_prod_book_chapter,
                ind_prod_software,
                ind_prod_granted_patent,
                ind_prod_not_granted_patent,
                ind_prod_report)
            VALUES (
                '{Data['graduate_program_id']}',
                {Intern_Data['year']},
                {Intern_Data['ind_prod_article']},
                {Intern_Data['ind_prod_book']},
                {Intern_Data['ind_prod_book_chapter']},
                {Intern_Data['ind_prod_software']},
                {Intern_Data['ind_prod_granted_patent']},
                {Intern_Data['ind_prod_not_granted_patent']},
                {Intern_Data['ind_prod_report']});
            """
            sgbdSQL.execScript_db(script_sql)
