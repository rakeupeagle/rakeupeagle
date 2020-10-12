# Django
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from app.models import Account
from app.models import Contact
from app.models import District
from app.models import Report
from app.models import School
from app.models import Student
from app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Set Cursor
        admin = User.objects.create(
            username='auth0|5f07d616a1f6030019b0a1ea',
            name='Admin',
            email='dbinetti@startnormal.com',
            is_active=True,
            is_admin=True,
        )
        user = User.objects.create(
            username='auth0|5f119d98de3b59001924ead8',
            name='Foo Bar',
            email='foo@startnormal.com',
            is_active=True,
            is_admin=False,
        )
        scsd = District.objects.create(
            name='San Carlos School District',
            status=District.STATUS.active,
            kind=District.KIND.elementary,
            nces_id=5400,
            address='123 Foo St',
            city='San Carlos',
            state='CA',
            website='https://foobar.com',
            lon=32.0,
            lat=-122.0,
        )

        central = School.objects.create(
            name='Central Middle',
            status=School.STATUS.active,
            level=School.LEVEL.intmidjr,
            nces_id=5405,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website='https://www.foobar.com',
            lon=32.0,
            lat=-122.0,
            district=scsd,
        )

        ba = School.objects.create(
            name='Brittan Acres',
            status=School.STATUS.active,
            level=School.LEVEL.elem,
            nces_id=5402,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website='https://www.foobar.com',
            lon=32.0,
            lat=-122.0,
            district=scsd,
        )
        Student.objects.create(
            grade=Student.GRADE.sixth,
            user=user,
            school=central,
        )
        Student.objects.create(
            grade=Student.GRADE.third,
            user=user,
            school=ba,
        )
        Contact.objects.create(
            name='Mao Harmeier',
            role=Contact.ROLE.super,
            district=scsd,
        )
        Report.objects.create(
            title='Bad news',
            status=Report.STATUS.approved,
            text="Now is the time for all good men to come to the aid of their schools!",
            district=scsd,
            user=user,
        )
        self.stdout.write("Complete.")
        return
