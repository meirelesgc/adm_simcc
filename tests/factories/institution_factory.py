import uuid
import factory
import factory.fuzzy
from random import randint


class InstitutionFactory(factory.Factory):
    class Meta:
        model = dict

    institution_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.fuzzy.FuzzyText(length=20)
    acronym = factory.fuzzy.FuzzyText(length=20)
    lattes_id = factory.Sequence(lambda n: f"{randint(0, 10 ** 15)}".zfill(16))


if __name__ == "__main__":
    from pprint import pprint

    pprint(InstitutionFactory.create_batch(3))
