import factory
import uuid
from random import randint


class GraduateProgramFactory(factory.Factory):
    class Meta:
        model = dict

    graduate_program_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    code = factory.Sequence(lambda n: f"GP {n + 1}")
    name = factory.Sequence(lambda n: f"Graduate Program {n + 1}")
    area = factory.Faker("word")
    modality = factory.Faker("word")
    type = factory.Faker("word")
    rating = factory.LazyFunction(lambda: str(randint(1, 5)))
    institution_id = factory.LazyFunction(lambda: uuid.uuid4())
    city = "Salvador"
    url_image = factory.Faker("url")
    sigla = factory.LazyFunction(lambda: f"GP{randint(1, 100)}")
    description = factory.Faker("text")
    visible = False
