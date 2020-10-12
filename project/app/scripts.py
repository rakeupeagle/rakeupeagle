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
# # from app.models import Contact
# from app.models import District
# from app.models import Homeroom
# from app.models import School
# from app.tasks import build_email
# from app.tasks import send_email
# from nameparser import HumanName

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

# def schools_list(filename='publics.csv'):
#     with open(filename) as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         next(reader)
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
#             funding_map = {
#                 'Directly funded': 10,
#                 'Locally funded': 20,
#                 'Disallowed': 30,
#             }
#             status_key = str(row[3]) if row[3] != 'No Data' else None
#             cd_status = status_map.get(status_key, None)
#             if cd_status != 10:
#                 continue
#             name = str(row[6]) if row[6] != 'No Data' else ''
#             if not name:
#                 continue
#             try:
#                 charter_number = int(row[25]) if row[25] != 'No Data' else None
#             except ValueError:
#                 charter_number = None
#             school = {
#                 'name': name,
#                 'cd_status': cd_status,
#                 'cd_id': int(row[0][-7:]) if row[0] != 'No Data' else None,
#                 'nces_district_id': int(row[1]) if row[1] != 'No Data' else None,
#                 'nces_school_id': int(row[2]) if row[2] != 'No Data' else None,
#                 'district_name': str(row[5]) if row[5] != 'No Data' else '',
#                 'county': str(row[4]) if row[4] != 'No Data' else '',
#                 'address': str(row[8]) if row[8] != 'No Data' else '',
#                 'city': str(row[9]) if row[9] != 'No Data' else '',
#                 'state': str(row[11]) if row[11] != 'No Data' else '',
#                 'zipcode': str(row[10]) if row[10] != 'No Data' else '',
#                 'phone': str(row[17]) if row[17] != 'No Data' else '',
#                 'website': str(row[21].replace(" ", "")) if row[21] != 'No Data' else '',
#                 # 'soc': int(row[29]) if row[29] != 'No Data' else None,

#                 'is_charter': True if row[24]=='Y' else False,
#                 'charter_number': charter_number,
#                 'funding_type': funding_map[str(row[26])] if row[26] != 'No Data' else None,
#                 # 'edops_type': getattr(School.EDOPS, str(row[31].strip().lower()), None),
#                 # 'eil': getattr(School.EIL, str(row[33].strip().lower()), None),
#                 'grade_span': str(row[35]) if row[35] != 'No Data' else '',
#                 # 'virtual_type': getattr(School.VIRTUAL, str(row[37].strip().lower()), None),
#                 'is_magnet': True if row[38]=='Y' else False,
#                 'fed_nces_school_id': int(row[40]) if row[40] != 'No Data' else None,

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
#             # form = SchoolForm(school)
#             # if not form.is_valid():
#             #     errors.append((row, form))
#             #     break
#             output.append(school)
#         if not errors:
#             return output
#         else:
#             print('Error!')
#             return errors

# def elsi_public_list(filename='publics.csv'):
#     with open(filename) as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         next(reader)
#         rows = [row for row in reader]
#         t = len(rows)
#         i = 0
#         errors = []
#         output = []
#         STATUS = {
#             '3-New': 0,
#             '1-Open': 10,
#             '2-Closed': 20,
#             '7-Future': None,
#             '6-Inactive': 20,
#             '5-Changed Boundary/Agency': 30,
#             '4-Added': None,
#             '8-Reopened': 10
#         }
#         GRADE = {
#             '6th Grade': 60,
#             '5th Grade': 50,
#             '9th Grade': 90,
#             '–': None,
#             'Prekindergarten': 2,
#             'Kindergarten': 5,
#             '10th Grade': 100,
#             '7th Grade': 70,
#             '4th Grade': 40,
#             '8th Grade': 80,
#             '3rd Grade': 30,
#             'Ungraded': None,
#             '1st Grade': 10,
#             '2nd Grade': 20,
#             '12th Grade': 120,
#             '11th Grade': 110,
#             '13th Grade': 130,
#             '†': None,
#             'Adult Education': None,
#         }
#         LEVEL = {
#             'High': 540,
#             'Middle': 530,
#             'Not Reported': None,
#             'Elementary': 520,
#             'Other': None,
#             'Prekindergarten': 510,
#             'Secondary': None,
#             'Ungraded': 570,
#             'Not Applicable': None,
#             'Adult Education': 560,
#          }
#         for row in rows:
#             i += 1
#             name = str(row[4]).strip()
#             status = STATUS[str(row[23]).strip()]
#             if status != 10:
#                 continue
#             level = LEVEL[str(row[32]).strip()]
#             nces_id = int(str(row[5]).strip())
#             try:
#                 low_grade = int(GRADE[str(row[33]).strip()])
#             except TypeError:
#                 low_grade = None
#             try:
#                 high_grade = int(GRADE[str(row[34]).strip()])
#             except TypeError:
#                 high_grade = None
#             address = str(row[12]).strip()
#             city = str(row[15]).strip()
#             state = str(row[16]).strip()
#             zipcode = str(row[17]).strip()
#             county = str(row[9]).strip()
#             phone = str(row[19]).strip()
#             website = str(row[6]).strip()
#             try:
#                 url_validator(website)
#             except ValidationError:
#                 website = ''
#             lat = float(row[28])
#             lon = float(row[29])
#             school = {
#                 'name': name,
#                 'status': status,
#                 'level': level,
#                 'low_grade': low_grade,
#                 'high_grade': high_grade,
#                 'address': address,
#                 'city': city,
#                 'state': state,
#                 'zipcode': zipcode,
#                 'county': county,
#                 'phone': phone,
#                 'website': website,
#                 'lat': lat,
#                 'lon': lon,
#             }
#             form = SchoolForm(school)
#             if form.is_valid():
#                 school, created = School.objects.update_or_create(
#                     nces_id=nces_id,
#                     defaults=school,
#                 )
#                 if created:
#                     print(f"{i}/{t} - created")
#                 else:
#                     print(f"{i}/{t} - updated")
#             else:
#                 output.append((school.state, school.id))
#     return output

# def elsi_private_list(filename='privates.csv'):
#     with open(filename) as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         next(reader)
#         rows = [row for row in reader]
#         t = len(rows)
#         i = 0
#         errors = []
#         output = []
#         GRADE = {
#             '6th grade': 60,
#             '5th grade': 50,
#             '9th grade': 90,
#             'Prekindergarten': 2,
#             'Kindergarten': 5,
#             'Transitional Kindergarten': 5,
#             '10th grade': 100,
#             '7th grade': 70,
#             '4th grade': 40,
#             '8th grade': 80,
#             '3rd grade': 30,
#             '1st grade': 10,
#             'Transitional 1st grade': 10,
#             '2nd grade': 20,
#             '12th grade': 120,
#             '11th grade': 110,
#             '†': None,
#             'All Ungraded': None,
#         }
#         LEVEL = {
#             '3': 550,
#             '1': 520,
#             '2': 555,
#             '†': None,
#          }
#         for row in rows:
#             i += 1
#             name = str(row[0]).strip()
#             status = 10
#             level = LEVEL[str(row[13]).strip()[0]]
#             nces_id = str(row[2]).strip()
#             low_grade = GRADE[str(row[10]).strip()]
#             high_grade = GRADE[str(row[11]).strip()]
#             address = str(row[7]).strip()
#             city = str(row[8]).strip()
#             state = str(row[9]).strip()
#             zipcode = str(row[14]).strip()
#             county = str(row[3]).strip()
#             phone = str(row[6]).strip()
#             website = ''
#             lat = None
#             lon = None
#             school = {
#                 'name': name,
#                 'status': status,
#                 'level': level,
#                 'nces_id': nces_id,
#                 'low_grade': low_grade,
#                 'high_grade': high_grade,
#                 'address': address,
#                 'city': city,
#                 'state': state,
#                 'zipcode': zipcode,
#                 'county': county,
#                 'phone': phone,
#                 'website': website,
#                 'lat': lat,
#                 'lon': lon,
#             }
#             form = SchoolForm(school)
#             if form.is_valid():
#                 form.save()
#             else:
#                 errors.append((form, row))
#             print(f"{i}/{t}")
#     return errors


# def import_schools(schools):
#     t = len(schools)
#     i = 0

#     for school in schools:
#         i+=1
#         print(f"{i}/{t}")
#         School.objects.create(**school)

# #private
# def private_districts_list(filename='privates.csv'):
#     with open(filename) as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         next(reader)
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
#             status_key = str(row[7]) if row[7] != 'No Data' else None
#             cd_status = status_map.get(status_key, None)
#             humanname = HumanName(str(row[37]) if row[37] != 'No Data' else '')
#             district = {
#                 'status': District.STATUS.active,
#                 'name': str(row[6]) if row[6] != 'No Data' else '',
#                 'kind': 470,
#                 'cd_id': int(row[1]) if row[1] != 'No Data' else None,
#                 'nces_id': int(row[2]) if row[2] != 'No Data' else None,
#                 # 'district_name': str(row[5]) if row[5] != 'No Data' else '',
#                 'address': str(row[25]) if row[25] != 'No Data' else '',
#                 'city': str(row[26]) if row[26] != 'No Data' else '',
#                 'state': str(row[27]) if row[27] != 'No Data' else '',
#                 'zipcode': str(row[28]) if row[28] != 'No Data' else '',
#                 'county': str(row[4]) if row[4] != 'No Data' else '',
#                 'phone': str(row[33]) if row[33] != 'No Data' else '',
#                 'website': str(row[22].replace(" ", "")) if row[21] != 'No Data' else '',
#                 'lat': float(row[23]) if row[23] != 'No Data' else None,
#                 'lon': float(row[24]) if row[24] != 'No Data' else None,

#                 # 'admin_first_name': humanname.first,
#                 # 'admin_last_name': humanname.last,
#                 # 'admin_email': str(row[40]) if row[40] not in [
#                 #     'Information Not Available',
#                 #     'No Data',
#                 # ] else '',
#                 # 'district': None,
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

# def import_private_districts(privates):
#     t = len(privates)
#     i = 0

#     for private in privates:
#         i+=1
#         print(f"{i}/{t}")
#         if private['cd_id'] == 77764229999999:
#             continue
#         District.objects.create(**private)

# def private_schools_list(filename='privates.csv'):
#     with open(filename) as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         next(reader)
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
#             kind_map = {
#                 'Elementary School (Private)': 520,
#                 'K-12 Schools (Private)': 550,
#                 'High Schools (Private)': 540,
#                 'Ungraded Schools (Private)': 570,
#                 'Kindergartens (Private)': 510,
#             }
#             status_key = str(row[7]) if row[7] != 'No Data' else None
#             cd_status = status_map.get(status_key, None)
#             humanname = HumanName(str(row[37]) if row[37] != 'No Data' else '')
#             cd_id = int(row[1]) if row[1] != 'No Data' else None
#             try:
#                 district = District.objects.get(cd_id=cd_id)
#             except District.DoesNotExist:
#                 continue
#             school = {
#                 'status': School.STATUS.active,
#                 'name': str(row[6]) if row[6] != 'No Data' else '',
#                 'level': level_map[row[14]] if row[14] != 'No Data' else None,
#                 'cd_id': cd_id,
#                 'nces_id': int(row[2]) if row[2] != 'No Data' else None,
#                 # 'district_name': str(row[5]) if row[5] != 'No Data' else '',
#                 'address': str(row[25]) if row[25] != 'No Data' else '',
#                 'city': str(row[26]) if row[26] != 'No Data' else '',
#                 'state': str(row[27]) if row[27] != 'No Data' else '',
#                 'zipcode': str(row[28]) if row[28] != 'No Data' else '',
#                 'county': str(row[4]) if row[4] != 'No Data' else '',
#                 'phone': str(row[33]) if row[33] != 'No Data' else '',
#                 'website': str(row[22].replace(" ", "")) if row[21] != 'No Data' else '',
#                 'lat': float(row[23]) if row[23] != 'No Data' else None,
#                 'lon': float(row[24]) if row[24] != 'No Data' else None,
#                 'low': str(row[15]) if row[15] != 'No Data' else None,
#                 'high': str(row[16]) if row[16] != 'No Data' else None,

#                 # 'admin_first_name': humanname.first,
#                 # 'admin_last_name': humanname.last,
#                 # 'admin_email': str(row[40]) if row[40] not in [
#                 #     'Information Not Available',
#                 #     'No Data',
#                 # ] else '',
#                 'district': district,
#             }
#             form = SchoolForm(school)
#             if not form.is_valid():
#                 errors.append((row, form))
#                 break
#             output.append(school)
#         if not errors:
#             return output
#         else:
#             print('Error!')
#             return errors

# def import_private_schools(privates):
#     t = len(privates)
#     i = 0

#     for private in privates:
#         i+=1
#         print(f"{i}/{t}")
#         if private['cd_id'] == 77764229999999:
#             continue
#         School.objects.create(**private)


# def private_contacts_list(filename='privates.csv'):
#     with open(filename) as f:
#         reader = csv.reader(
#             f,
#             skipinitialspace=True,
#         )
#         next(reader)
#         rows = [row for row in reader]
#         t = len(rows)
#         i = 0
#         errors = []
#         output = []
#         for row in rows:
#             i += 1
#             print(f"{i}/{t}")
#             cd_id = int(row[1]) if row[1] != 'No Data' else None
#             if cd_id == 77764229999999:
#                 continue
#             try:
#                 school = School.objects.get(cd_id=cd_id)
#             except School.DoesNotExist:
#                 print(row)
#                 break
#             contact = {
#                 'name': str(row[6]) if row[6] != 'No Data' else '',
#                 'phone': str(row[33]) if row[33] != 'No Data' else '',
#                 'name': str(row[37]) if row[37] != 'No Data' else '',
#                 'role': Contact.ROLE.admin,
#                 'email': str(row[40]) if row[40] not in [
#                     'Information Not Available',
#                     'No Data',
#                 ] else '',
#                 'school': school.id,
#             }
#             form = ContactForm(contact)
#             if not form.is_valid():
#                 continue
#             output.append(contact)
#         if not errors:
#             return output
#         else:
#             print('Error!')
#             return errors


# def import_private_contacts(privates):
#     t = len(privates)
#     i = 0

#     for private in privates:
#         i+=1
#         print(f"{i}/{t}")
#         school_id = private['school']
#         school = School.objects.get(id=school_id)
#         private.pop('school')
#         contact, created = Contact.objects.get_or_create(**private)
#         Entry.objects.create(
#             school=school,
#             contact=contact,
#         )


# def import_public_contacts(publics):
#     t = len(publics)
#     i = 0
#     errors = []
#     for public in publics:
#         i+=1
#         print(f"{i}/{t}")
#         try:
#             school = School.objects.get(nces_id=public['nces_school_id'])
#         except School.DoesNotExist:
#             continue
#         except School.MultipleObjectsReturned:
#             continue
#         name = " ".join([
#             public['admin_first_name'],
#             public['admin_last_name'],
#         ])
#         contact = {
#             'name': name,
#             'email': public['admin_email'],
#             'phone': public['phone'],
#             'role': Contact.ROLE.principal,
#         }
#         form = ContactForm(contact)
#         if form.is_valid():
#             contact = form.save()
#             Entry.objects.create(
#                 school=school,
#                 contact=contact,
#             )
#     return


# def post_welcome(user):
#     email = build_email(
#         template='emails/welcome.txt',
#         subject='A Belated Welcome to Start Normal!',
#         to=[user.email],
#         bcc=['dbinetti@startnormal.com'],
#         html_content='emails/welcome.html',
#     )
#     send_email.delay(email)


# def announce_homerooms(user):
#     email = build_email(
#         template='emails/homerooms.txt',
#         subject='[Start Normal] Introducing Homerooms',
#         to=[user.email],
#         bcc=['dbinetti@startnormal.com'],
#         # html_content='emails/homerooms.html',
#     )
#     send_email.delay(email)


# def import_grades(s):
#     mapping = {
#         'P': 2,
#         'K': 5,
#         '1': 10,
#         '2': 20,
#         '3': 30,
#         '4': 40,
#         '5': 50,
#         '6': 60,
#         '7': 70,
#         '8': 80,
#         '9': 90,
#         '10':100,
#         '11': 110,
#         '12': 120,
#         '13': None,
#         'Post Secondary': None,
#         '': None,
#         'Adult': None,
#         None: None,
#     }


#     parts = s['grade_span'].partition('-')
#     low = parts[0].strip()
#     high = parts[2].strip()
#     if low == 'Adult' or high == 'Adult':
#         return
#     if not high:
#         high = low
#     high_grade = mapping[str(high)]
#     low_grade = mapping[str(low)]

#     if not high_grade and not low_grade:
#         print('none')
#         return
#     try:
#         c = School.objects.get(nces_id=s['nces_school_id'])
#     except School.DoesNotExist:
#         print('n')
#         return
#     except School.MultipleObjectsReturned:
#         return
#     c.high_grade = high_grade
#     c.low_grade = low_grade
#     c.save()
#     print('saved')

# def import_private_grades(s):
#     mapping = {
#         'P': 2,
#         'K': 5,
#         '1': 10,
#         '2': 20,
#         '3': 30,
#         '4': 40,
#         '5': 50,
#         '6': 60,
#         '7': 70,
#         '8': 80,
#         '9': 90,
#         '10':100,
#         '11': 110,
#         '12': 120,
#     }


#     low = s['low']
#     high = s['high']
#     try:
#         high_grade = mapping[str(high)]
#     except KeyError:
#         print('skip high')
#         return
#     try:
#         low_grade = mapping[str(low)]
#     except KeyError:
#         print('skip low')
#         return

#     try:
#         c = School.objects.get(cd_id=s['cd_id'])
#     except School.DoesNotExist:
#         print('n')
#         return
#     except School.MultipleObjectsReturned:
#         return
#     c.high_grade = high_grade
#     c.low_grade = low_grade
#     c.save()
#     print('saved')


# def create_homerooms():
#     i = 0
#     ss = School.objects.filter(
#         low_grade__isnull=False,
#         high_grade__isnull=False,
#     )
#     errors = []
#     for s in ss:
#         i+=1
#         grades = [2,5,10,20,30,40,50,60,70,80,90,100,110,120]
#         for grade in grades:
#             if grade >= s.low_grade and grade <= s.high_grade:
#                 grade_name = School.GRADE[grade]
#                 name = "{0} {1}".format(
#                     s.name,
#                     grade_name,
#                 )
#                 defaults = {
#                     'name': name,
#                 }
#                 try:
#                     h, _ = Homeroom.objects.update_or_create(
#                         grade=grade,
#                         school=s,
#                         defaults=defaults,
#                     )
#                 except Homeroom.MultipleObjectsReturned:
#                     errors.append((s, grade))
#                     continue
#                 print(i, grade, h)
