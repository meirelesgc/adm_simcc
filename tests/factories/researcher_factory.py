import factory
import uuid
from random import randint
from faker import Factory as FakerFactory


faker = FakerFactory.create()


class ResearcherFactory(factory.Factory):
    class Meta:
        model = dict

    researcher_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Sequence(lambda n: f"Pesquisador - {n + 1}")
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
    id_lattes = factory.LazyAttribute(lambda _: faker.uuid4())
    nome_beneficiario = factory.LazyAttribute(lambda _: faker.name())
    cpf_beneficiario = factory.LazyAttribute(lambda _: faker.ssn())
    nome_pais = factory.LazyAttribute(lambda _: faker.country())
    nome_regiao = factory.LazyAttribute(
        lambda _: faker.random_element(
            elements=("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")
        )
    )
    nome_uf = factory.LazyAttribute(lambda _: faker.state())
    nome_cidade = factory.LazyAttribute(lambda _: faker.city())
    nome_grande_area = factory.LazyAttribute(
        lambda _: faker.random_element(
            elements=(
                "Ciências Exatas e da Terra",
                "Ciências Biológicas",
                "Engenharias",
                "Ciências da Saúde",
                "Ciências Agrárias",
                "Ciências Sociais Aplicadas",
                "Ciências Humanas",
                "Linguística, Letras e Artes",
            )
        )
    )
    nome_area = factory.LazyAttribute(lambda _: faker.job())
    nome_sub_area = factory.LazyAttribute(lambda _: faker.job())
    cod_modalidade = factory.LazyAttribute(
        lambda _: faker.random_element(elements=("A", "B", "C", "D"))
    )
    nome_modalidade = factory.LazyAttribute(
        lambda _: faker.random_element(
            elements=(
                "Bolsa de Iniciação Científica",
                "Bolsa de Mestrado",
                "Bolsa de Doutorado",
                "Auxílio à Pesquisa",
            )
        )
    )
    titulo_chamada = factory.LazyAttribute(lambda _: faker.sentence())
    cod_categoria_nivel = factory.LazyAttribute(lambda _: str(randint(1, 5)))
    nome_programa_fomento = factory.LazyAttribute(lambda _: faker.company())
    nome_instituto = factory.LazyAttribute(lambda _: faker.company())
    quant_auxilio = factory.LazyAttribute(lambda _: randint(1000, 5000))
    quant_bolsa = factory.LazyAttribute(lambda _: randint(1, 5))
