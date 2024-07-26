from factory import Factory, LazyFunction, Sequence, Faker, LazyAttribute
from uuid import uuid4
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class ResearchGroupFactory(Factory):
    class Meta:
        model = dict

    nome_grupo = Sequence(lambda n: f"Grupo de pesquisa - {n + 1}")
    nome_lider = Sequence(lambda n: f"Lider - {n + 1}")
    area = Faker("word")
    ultimo_envio = LazyFunction(
        lambda: faker.date_between(start_date="-5y", end_date="today").strftime(
            "%d/%m/%Y"
        )
    )
    situacao = LazyAttribute(
        lambda n: faker.random_element(
            elements=("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")
        )
    )
    institution_id = LazyFunction(lambda: str(uuid4()))
