import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Collection
import uuid


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.LazyFunction(lambda: make_password('password123'))


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    uuid = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')

