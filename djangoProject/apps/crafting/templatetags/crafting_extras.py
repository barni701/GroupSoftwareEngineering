# apps/crafting/templatetags/crafting_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieve dictionary value using a key."""
    return dictionary.get(str(key), 0)