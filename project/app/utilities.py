# Utility
def export_teams_csv():
    ts = Team.objects.all()
    with open('teams.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name',
            'Phone',
            'State',
            'Size',
            'Nickname',
            'Reference',
            'Notes',
            'Admin Notes',
        ])
        for t in ts:
            writer.writerow([
                t.name,
                t.phone,
                t.state,
                t.size,
                t.nickname,
                t.reference,
                t.public_notes,
                t.admin_notes,
            ])


def import_teams_csv():
    with open('teams.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                user = User.objects.get(
                    phone=row[1],
                )
            except User.DoesNotExist:
                user = None
            Team.objects.create(
                name = row[0],
                phone = row[1],
                state = row[2],
                size = row[3],
                nickname = row[4],
                reference = row[5],
                notes = row[6],
                admin_notes = row[7],
                user=user,
            )


def export_recipients_csv():
    rs = Recipient.objects.all()
    with open('recipients.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name',
            'Phone',
            'State',
            'Size',
            'Location',
            'Place',
            'Is Precise',
            # 'Point',
            'Geocode',
            'Is Dog',
            'Notes',
            'Admin Notes',
        ])
        for r in rs:
            writer.writerow([
                r.name,
                r.phone,
                r.state,
                r.size,
                r.location,
                r.place,
                r.is_precise,
                # r.point,
                r.geocode,
                r.is_dog,
                r.public_notes,
                r.admin_notes,
            ])


def import_recipients_csv():
    with open('recipients.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                user = User.objects.get(
                    phone=row[1],
                )
            except User.DoesNotExist:
                user = None
            Recipient.objects.create(
                name = row[0],
                phone = row[1],
                state = row[2],
                size = row[3],
                location = row[4],
                place = row[5],
                is_precise = bool(row[6]),
                geocode = row[7],
                is_dog = bool(row[8]),
                notes = row[9],
                admin_notes = row[10],
                user=user,
            )


def export_assignments_csv():
    gs = Assignment.objects.all()
    with open('assignments.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Recipient',
            'Team',
        ])
        for g in gs:
            writer.writerow([
                g.recipient.name,
                g.team.name,
            ])


def import_assignments_csv():
    with open('assignments.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            recipient = Recipient.objects.get(
                name=row[0],
            )
            team = Team.objects.get(
                name=row[1],
            )
            Assignment.objects.create(
                recipient=recipient,
                team=team,
            )


# def import_messages_csv():
#     with open('messages.csv', 'r') as f:
#         reader = csv.reader(f)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             status = row[3]
#             if status == 'delivered':
#                 direction = Message.DIRECTION.outbound
#                 phone = row[1]
#             elif status == 'received':
#                 direction = Message.DIRECTION.inbound
#                 phone = row[0]
#             else:
#                 raise Exception
#             if phone == '14157132126':
#                 continue
#             try:
#                 user = User.objects.get(
#                     phone=phone,
#                 )
#             except User.DoesNotExist:
#                 user = None
#             created = parser.parse(row[4])
#             Message.objects.create(
#                 to_phone=row[1],
#                 from_phone=row[0],
#                 sid=row[9],
#                 body=row[2],
#                 direction=direction,
#                 created=created,
#                 user=user,
#             )



# def import_r_calls_csv():
#     with open('r.csv', 'r') as f:
#         reader = csv.reader(f)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             name = row[0]
#             notes = row[5]
#             try:
#                 recipient = Recipient.objects.get(
#                     name=name,
#                 )
#             except Recipient.DoesNotExist:
#                 print(row[0])
#             recipient.admin_notes = notes
#             recipient.save()


# def import_t_calls_csv():
#     with open('t.csv', 'r') as f:
#         reader = csv.reader(f)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             name = row[0]
#             notes = row[4]
#             try:
#                 team = Team.objects.get(
#                     name=name,
#                 )
#             except Team.DoesNotExist:
#                 print(row[0])
#             team.admin_notes = notes
#             team.save()


# def get_messages_csv():
#     ms = Message.objects.all()
#     with open('messages.csv', 'w') as f:
#         writer = csv.writer(f)
#         writer.writerow([
#             'SID',
#             'To Phone',
#             'From Phone',
#             'Body',
#             'Direction',
#             'Raw',
#             'Created',
#         ])
#         for m in ms:
#             writer.writerow([
#                 m.sid,
#                 m.to_phone,
#                 m.from_phone,
#                 m.body,
#                 m.direction,
#                 m.raw,
#                 m.created,
#             ])

