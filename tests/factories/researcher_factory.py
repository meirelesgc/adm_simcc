import factory
import factory.fuzzy

import uuid
from random import randint


class ResearcherFactory(factory.Factory):
    class Meta:
        model = dict

    researcher_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.fuzzy.FuzzyText(length=20)
    lattes_id = factory.Sequence(lambda n: f"{randint(0, 10 ** 15)}".zfill(16))
    institution_id = factory.LazyFunction(lambda: str(uuid.uuid4()))


class FullResearcherFactory(ResearcherFactory):
    subsidies = [
        {
            "category_level_code": None,
            "modality_code": None,
            "subsidy_id": None,
        }
    ]


class SubsidiesFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    id_lattes = factory.fuzzy.FuzzyText(length=20)
    nome_beneficiario = factory.fuzzy.FuzzyText(length=20)
    cpf_beneficiario = factory.fuzzy.FuzzyText(length=20)
    nome_pais = factory.fuzzy.FuzzyText(length=20)
    nome_regiao = factory.fuzzy.FuzzyText(length=20)
    nome_uf = factory.fuzzy.FuzzyText(length=20)
    nome_cidade = factory.fuzzy.FuzzyText(length=20)
    nome_grande_area = factory.fuzzy.FuzzyText(length=20)
    nome_area = factory.fuzzy.FuzzyText(length=20)
    nome_sub_area = factory.fuzzy.FuzzyText(length=20)
    cod_modalidade = factory.fuzzy.FuzzyText(length=20)
    nome_modalidade = factory.fuzzy.FuzzyText(length=20)
    titulo_chamada = factory.fuzzy.FuzzyText(length=20)
    cod_categoria_nivel = factory.fuzzy.FuzzyText(length=20)
    nome_programa_fomento = factory.fuzzy.FuzzyText(length=20)
    nome_instituto = factory.fuzzy.FuzzyText(length=20)
    quant_auxilio = factory.fuzzy.FuzzyText(length=20)
    quant_bolsa = factory.LazyFunction(lambda: randint(0, 10))


if __name__ == "__main__":
    from pprint import pprint

    pprint(SubsidiesFactory.create_batch(3))
