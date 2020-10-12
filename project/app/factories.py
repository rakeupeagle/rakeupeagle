# # Django
# from django.db.models.signals import post_delete
# from django.db.models.signals import post_save

# # First-Party
# from factory import Faker  # post_generation,
# from factory import PostGenerationMethodCall
# from factory import RelatedFactory
# from factory import SubFactory
# from factory.django import DjangoModelFactory
# from factory.django import mute_signals

# # Local
# from .models import Account
# from .models import School
# from .models import User


# class AccountFactory(DjangoModelFactory):
#     is_welcomed = True
#     user = SubFactory(
#         'app.factories.UserFactory',
#     )
#     class Meta:
#         model = Account


# class SchoolFactory(DjangoModelFactory):
#     name = 'Central Middle'
#     status = School.STATUS.active
#     level = School.LEVEL.intmidjr
#     nces_id = 5401
#     address = '123 Main St'
#     city = 'San Carlos'
#     state = 'CA'
#     website = Faker('url')
#     lon = 32.0
#     lat = -122.0
#     class Meta:
#         model = School


# @mute_signals(post_delete, post_save)
# class UserFactory(DjangoModelFactory):
#     name = Faker('name_male')
#     email = Faker('email')
#     password = PostGenerationMethodCall('set_unusable_password')
#     is_active = True
#     class Meta:
#         model = User
