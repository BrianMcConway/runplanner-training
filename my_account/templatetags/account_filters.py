from django import template

register = template.Library()


@register.filter
def replace_underscore(value):
    """Replaces underscores with spaces and capitalizes words."""
    return value.replace('_', ' ').title()
