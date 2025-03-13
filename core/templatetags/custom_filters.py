from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Fetch a dictionary value using a key in templates."""
    return dictionary.get(key, "Not Answered")
