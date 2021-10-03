from django import template
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import PhoneNumberFormat

register = template.Library()

@register.filter(name='phonenumber')
def phonenumber(value):
    if isinstance(value, PhoneNumber):
        formatter = PhoneNumberFormat.NATIONAL
        return value.format_as(formatter)
    return value
