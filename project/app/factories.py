# First-Party
from factory import Faker
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory

# Local
from .models import User


class UserFactory(DjangoModelFactory):
    name = Faker('name_male')
    phone = Faker('phone_number')
    password = PostGenerationMethodCall('set_unusable_password')
    is_active = True
    class Meta:
        model = User
