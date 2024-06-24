import factory
import uuid
from random import randint


class InstitutionFactory(factory.Factory):
    class Meta:
        model = dict

    institution_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Sequence(lambda n: f"Instituição - {n + 1}")
    acronym = factory.Sequence(lambda n: f"IN{n + 1}")
    lattes_id = factory.Sequence(lambda n: f"{randint(0, 10 ** 11)}".zfill(12))
