import factory
import uuid
from random import randint
from datetime import datetime


class StudentFactory(factory.Factory):
    class Meta:
        model = dict

    student_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Sequence(lambda n: f"Estudante - {n + 1}")
    lattes_id = factory.Sequence(lambda n: f"{randint(0, 10 ** 15)}".zfill(16))
    institution_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    graduate_program_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    year = factory.LazyFunction(lambda: randint(2000, datetime.now().year))
