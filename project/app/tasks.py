import geocoder
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django_rq import job


# Geocoding
def get_precision(geocode):
    return all([
        geocode['accuracy'] == 'ROOFTOP',
        any([
            geocode['quality'] == 'premise',
            geocode['quality'] == 'subpremise',
            geocode['quality'] == 'street_address',
        ])
    ])


@job
def geocode_recipient(recipient):
    address = f"{recipient.location}, Eagle, ID"
    result = geocoder.google(address)
    geocode = result.json
    try:
        is_precise = get_precision(geocode)
    except TypeError:
        return
    if is_precise:
        recipient.point = Point(
            geocode['lng'],
            geocode['lat'],
        )
        recipient.save()
    return


# Messaging
@job
def send_instance_message(instance, message):
    body = render_to_string(
        f'app/texts/{message}.txt',
        context={
            'instance': instance,
        },
    )
    message = instance.messages.create(
        body=body,
    )
    return message
