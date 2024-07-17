import factory
from factory import fuzzy
import random


class TeacherFactory(factory.Factory):
    class Meta:
        model = dict

    matric = factory.Sequence(lambda n: 1131233 + n)
    inscUFMG = factory.Sequence(lambda n: 129132 + n)
    nome = factory.Faker("name")
    genero = factory.fuzzy.FuzzyChoice(["MASCULINO", "FEMININO"])
    situacao = factory.fuzzy.FuzzyChoice(["ATIVO PERMANENTE", "INATIVO", "APOSENTADO"])
    rt = factory.fuzzy.FuzzyChoice(["DE", "DT", "RT"])
    clas = factory.Sequence(lambda n: 7 + n)
    cargo = factory.fuzzy.FuzzyChoice(
        ["PROFESSOR DO MAGISTERIO SUPERIOR", "PESQUISADOR"]
    )
    classe = factory.fuzzy.FuzzyChoice(
        ["PROFESSOR DO MAGISTERIO SUPERIOR", "PROF TITULAR"]
    )
    ref = factory.Sequence(lambda n: 704 + n)
    titulacao = factory.fuzzy.FuzzyChoice(["DOUTORADO", "MESTRADO", "GRADUAÇÃO"])
    entradaNaUFMG = factory.Faker("date_this_century", before_today=True)
    progressao = factory.Faker("date_this_century", before_today=True)
    year_charge = factory.Faker("year")
    semester = factory.LazyAttribute(lambda x: random.randint(1, 2))
