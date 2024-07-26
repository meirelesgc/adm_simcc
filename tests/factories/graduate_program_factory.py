import uuid
import factory
import factory.fuzzy
from random import randint


class GraduateProgramFactory(factory.Factory):
    class Meta:
        model = dict

    graduate_program_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    code = factory.fuzzy.FuzzyText(length=20)
    name = factory.fuzzy.FuzzyText(length=20)
    area = factory.fuzzy.FuzzyText(length=20)
    modality = factory.fuzzy.FuzzyText(length=20)
    type = factory.fuzzy.FuzzyText(length=20)
    rating = factory.LazyFunction(lambda: str(randint(1, 5)))
    institution_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    city = "Salvador"
    url_image = factory.fuzzy.FuzzyText(length=20)
    sigla = factory.fuzzy.FuzzyText(length=20)
    description = factory.fuzzy.FuzzyText(length=20)
    visible = False
