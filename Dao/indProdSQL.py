import pandas as pd
from pydantic import UUID4

import Dao.dbHandler as dbHandler
from Model.weights import Weights


def insert_ind_prod(weights: Weights):

    script_sql = f"""SELECT COUNT(*) FROM weights WHERE institution_id = '{weights.institution_id}'"""
    
    if (dbHandler.db_select(script_sql=script_sql)[0][0]):
        script_sql = f""""
            UPDATE public.weights
            SET 
                a1 = {weights.A1}, 
                a2 = {weights.A2}, 
                a3 = {weights.A3}, 
                a4 = {weights.A4}, 
                b1 = {weights.B1},
                b2 = {weights.B2}, 
                b3 = {weights.B3}, 
                b4 = {weights.B4}, 
                c = {weights.C},
                sq = {weights.SQ}, 
                book = {weights.BOOK},
                book_chapter = {weights.BOOK_CHAPTER}, 
                f1 = '{weights.F1}', 
                f2 = '{weights.F2}', 
                f3 = '{weights.F3}', 
                f4 = '{weights.F4}', 
                f5 = '{weights.F5}',
                software = '{weights.SOFTWARE}', 
                patent_granted = '{weights.PATENT_GRANTED}',
                patent_not_granted = '{weights.PATENT_NOT_GRANTED}', 
                report = '{weights.REPORT}'
            WHERE institution_id = '{weights.institution_id}';
        """
        dbHandler.db_script(script_sql=script_sql)
        return 
        
    
    script_sql = f"""
        INSERT INTO public.weights(
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
            '{weights.REPORT}'
            );
        """

    dbHandler.db_script(script_sql=script_sql)


def ind_prod_basic_query(institution_id):
    script_sql = f"""
        SELECT 
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
