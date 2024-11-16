import markdown
from django import template

register = template.Library()

@register.filter
def markdownify(text):
    """
    Converts Markdown text to HTML.
    """
    return markdown.markdown(text, extensions=["extra", "codehilite", "toc"])
