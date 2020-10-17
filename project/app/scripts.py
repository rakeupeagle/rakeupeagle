# # Standard Library
# import csv

# # Django
# from django.core.exceptions import ValidationError
# from django.core.validators import URLValidator
# from django.db import IntegrityError
# from django.db.models import Q

# # First-Party
# # from app.forms import ContactForm
# from app.forms import DistrictForm
# from app.forms import SchoolForm
# # from app.models import Entry
# from nameparser import HumanName

# First-Party
# # from app.models import Contact
# from app.models import District
# from app.models import Homeroom
# from app.models import School
from app.tasks import build_email
from app.tasks import send_email

# url_validator = URLValidator()
# # public
# def districts_list():
#     with open('ca.csv') as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         rows = [row for row in reader]
#         t = len(rows)
#         i = 0
#         errors = []
#         output = []
#         for row in rows:
#             i += 1
#             print(f"{i}/{t}")
#             status_map = {
#                 'Active': 10,
#                 'Closed': 20,
#                 'Merged': 30,
#             }
#             status_key = str(row[3]) if row[3] != 'No Data' else None
#             cd_status = status_map.get(status_key, None)

#             district = {
#                 'schedule': 0,
#                 'masks': 0,
#                 'cd_status': cd_status,
#                 'name': str(row[5]) if row[5] != 'No Data' else '',
#                 'cd_id': int(row[0][:7]) if row[0] != 'No Data' else None,
#                 'nces_district_id': int(row[1]) if row[1] != 'No Data' else None,
#                 'district_name': str(row[5]) if row[5] != 'No Data' else '',
#                 'county': str(row[4]) if row[4] != 'No Data' else '',
#                 'address': str(row[8]) if row[8] != 'No Data' else '',
#                 'city': str(row[9]) if row[9] != 'No Data' else '',
#                 'state': str(row[11]) if row[11] != 'No Data' else '',
#                 'zipcode': str(row[10]) if row[10] != 'No Data' else '',
#                 'phone': str(row[17]) if row[17] != 'No Data' else '',
#                 'website': str(row[21].replace(" ", "")) if row[21] != 'No Data' else '',
#                 'doc': int(row[27]) if row[27] != 'No Data' else None,
#                 'latitude': float(row[41]) if row[41] != 'No Data' else None,
#                 'longitude': float(row[42]) if row[42] != 'No Data' else None,
#                 'admin_first_name': str(row[43]) if row[43] != 'No Data' else '',
#                 'admin_last_name': str(row[44]) if row[44] != 'No Data' else '',
#                 'admin_email': str(row[45].replace(
#                     ' ', ''
#                 ).replace(
#                     'ndenson@compton.k12.ca.u', 'ndenson@compton.k12.ca.us'
#                 ).replace(
#                     'bmcconnell@compton.k12.ca.u', 'bmcconnell@compton.k12.ca.us'
#                 )) if row[45] not in [
#                     'Information Not Available',
#                     'No Data',
#                 ] else '',
#             }
#             form = DistrictForm(district)
#             if not form.is_valid():
#                 errors.append((row, form))
#                 break
#             output.append(district)
#         if not errors:
#             return output
#         else:
#             print('Error!')
#             return errors

# def import_districts(districts):
#     t = len(districts)
#     i = 0

#     for district in districts:
#         i+=1
#         print(f"{i}/{t}")
#         try:
#             District.objects.create(**district)
#         except IntegrityError:
#             continue


def send_confirmation(recipient):
    email = build_email(
        template='emails/confirmed.txt',
        subject='Rake Up Eagle Confirmation',
        to=[recipient.email],
        bcc=['dbinetti@gmail.com'],
        # html_content='emails/homerooms.html',
    )
    send_email.delay(email)
