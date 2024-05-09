import pandas as pd
from pydantic import UUID4

import Dao.dbHandler as dbHandler
from Model.weights import Weights


def insert_ind_prod(weights: Weights):
    script_sql = f"""
        INSERT INTO public.weights(
            name, 
            institution_id, 
            a1, 
            a2, 
            a3, 
            a4, 
            b1,
            b2, 
            b3, 
            b4, 
            c,
            sq, 
            book,
            book_chapter, 
            f1, 
            f2, 
            f3, 
            f4, 
            f5,
            software, 
            patent_granted, 
            patent_not_granted, 
            report)
        VALUES (
            '{weights.name}', 
            '{weights.institution_id}', 
            {weights.A1}, 
            {weights.A2}, 
            {weights.A3}, 
            {weights.A4}, 
            {weights.B1}, 
            {weights.B2}, 
            {weights.B3}, 
            {weights.B4}, 
            {weights.C}, 
            {weights.SQ}, 
            {weights.BOOK}, 
            {weights.BOOK_CHAPTER}, 
            '{weights.F1}', 
            '{weights.F2}', 
            '{weights.F3}', 
            '{weights.F4}', 
            '{weights.F5}',
            '{weights.SOFTWARE}',
            '{weights.PATENT_NOT_GRANTED}',
            '{weights.PATENT_GRANTED}',
            '{weights.REPORT}',
            );
        """

    dbHandler.db_script(script_sql=script_sql)


def ind_prod_basic_query(institution_id):
    script_sql = f"""
        SELECT 
            id, 
            name, 
            institution_id, 
            a1, a2, a3, a4, 
            b1, b2, b3, b4, 
            c, 
            sq, 
            book, 
            book_chapter, 
            f1, f2, f3, f4, f5
            software, 
            patent_granted, 
            patent_not_granted, 
            report
        FROM 
            public.weights
        WHERE institution_id = '{institution_id}';
        """
    registry = dbHandler.db_select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "id",
            "name",
            "institution_id",
            "a1",
            "a2",
            "a3",
            "a4",
            "b1",
            "b2",
            "b3",
            "b4",
            "c",
            "sq",
            "book",
            "book_chapter",
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "software",
            "patent_granted",
            "patent_not_granted",
            "report",
        ],
    )

    return data_frame.to_dict(orient="records")


def ind_prod_delete(weight_id: UUID4):
    script_sql = f"""
        DELETE FROM public.weights
        WHERE weight_id = '{weight_id}';
        """
    dbHandler.db_script(script_sql)
