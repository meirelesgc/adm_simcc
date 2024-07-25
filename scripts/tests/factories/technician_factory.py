import factory
from datetime import datetime
import random


class TechnicianFactory(factory.Factory):
    class Meta:
        model = dict

    matric = factory.Sequence(lambda n: 1001698 + n)
    ins_ufmg = factory.Sequence(lambda n: 49916116 + n)
    nome = factory.Faker("name")
    genero = factory.Iterator(["MASCULINO", "FEMININO"])
    deno_sit = factory.Iterator(["ATIVO PERMANENTE", "INATIVO"])
    rt = factory.Iterator(["40H", "20H"])
    classe = factory.Iterator(["A", "B", "C", "D", "E"])
    cargo = factory.Iterator(
        ["MESTRE EDIF E INFRAEST", "AUX EM ADMINIST", "ANALISTA DE SISTEMAS"]
    )
    nivel = factory.Iterator(["NIVEL INTERMEDIARIO", "NIVEL SUPERIOR"])
    ref = factory.Iterator(["416", "116", "216"])
    titulacao = factory.Iterator(
        ["ESPECIALIZAÇÃO", "MESTRADO", "DOUTORADO", "NÃO ESPECIFICADO"]
    )
    setor = factory.Iterator(["DEPARTAMENTO", "INSTITUTO"])
    detalhe_setor = factory.Iterator(
        ["ENG-DEPTO ENG MECANICA-SECRETARIA", "ENG-DEPTO ENG MAT CONST CIVIL"]
    )
    dting_org = factory.LazyFunction(
        lambda: datetime.strptime("21-jun-76", "%d-%b-%y").date()
    )
    data_prog = factory.LazyFunction(
        lambda: datetime.strptime("29/06/2006", "%d/%m/%Y").date()
    )
    year_charge = factory.Faker("year")
    semester = factory.LazyAttribute(lambda x: random.randint(1, 2))

    @factory.post_generation
    def format_dates(obj, create, extracted, **kwargs):
        obj["data_prog"] = obj["data_prog"].strftime("%d/%m/%Y")
        obj["dting_org"] = obj["dting_org"].strftime("%d/%m/%Y")


if __name__ == "__main__":
    from pprint import pprint

    pprint(TechnicianFactory.create_batch(1))
