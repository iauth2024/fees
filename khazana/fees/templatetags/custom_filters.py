# fees/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='indian_number_format')
def indian_number_format(value):
    """
    Converts a number into Indian format: 12,34,567
    """
    try:
        value = int(float(value))  # Convert to float first to handle decimal strings, then to int
    except ValueError:
        return value

    orig = str(value)
    if len(orig) <= 3:
        return orig

    # Separate the last 3 digits
    last_three = orig[-3:]
    # Get the rest of the digits
    other_digits = orig[:-3]

    # Split other_digits into groups of 2
    groups = []
    while other_digits:
        groups.append(other_digits[-2:])
        other_digits = other_digits[:-2]

    # Combine groups and last three digits
    formatted = ','.join(reversed(groups)) + ',' + last_three
    return formatted
