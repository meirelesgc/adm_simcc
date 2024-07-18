import factory
from factory import fuzzy
import random
from datetime import datetime


class TeacherFactory(factory.Factory):
    class Meta:
        model = dict

    matric = factory.Sequence(lambda n: 1131233 + n)
    inscUFMG = factory.Sequence(lambda n: 129132 + n)
    nome = factory.Faker("name")
    genero = fuzzy.FuzzyChoice(["MASCULINO", "FEMININO"])
    situacao = fuzzy.FuzzyChoice(["ATIVO PERMANENTE", "INATIVO", "APOSENTADO"])
    rt = fuzzy.FuzzyChoice(["DE", "DT", "RT"])
    clas = factory.Sequence(lambda n: 7 + n)
    cargo = fuzzy.FuzzyChoice(["PROFESSOR DO MAGISTERIO SUPERIOR", "PESQUISADOR"])
    classe = fuzzy.FuzzyChoice(["PROFESSOR DO MAGISTERIO SUPERIOR", "PROF TITULAR"])
    ref = factory.Sequence(lambda n: 704 + n)
    titulacao = fuzzy.FuzzyChoice(["DOUTORADO", "MESTRADO", "GRADUAÇÃO"])
    entradaNaUFMG = factory.Faker("date_this_century", before_today=True)
    progressao = factory.Faker("date_this_century", before_today=True)
    year_charge = factory.Faker("year")
    semester = factory.LazyAttribute(lambda x: random.randint(1, 2))

    @factory.post_generation
    def format_dates(obj, create, extracted, **kwargs):
        obj["entradaNaUFMG"] = obj["entradaNaUFMG"].strftime("%d/%m/%Y")
        obj["progressao"] = obj["progressao"].strftime("%d/%m/%Y")


if __name__ == "__main__":
    from pprint import pprint

    pprint(TeacherFactory.create_batch(1))
