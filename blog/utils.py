# blog/utils.py

import bleach
from markdown import markdown
from django.conf import settings

def sanitize_markdown(markdown_content):
    # Convert the frozenset to a list
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [
        'p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'br', 'pre', 'code', 'img', 'blockquote',
    ]

    allowed_attributes = dict(bleach.sanitizer.ALLOWED_ATTRIBUTES)
    allowed_attributes.update({
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title'],
        '*': ['class', 'style'],
    })

    # Convert Markdown to HTML
    html_content = markdown(
        markdown_content, extensions=settings.MARKDOWNX_MARKDOWN_EXTENSIONS
    )

    # Sanitize HTML content
    cleaned_content = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,
    )
    return cleaned_content
