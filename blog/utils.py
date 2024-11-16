import bleach
from markdown import markdown
from django.conf import settings
from bleach.css_sanitizer import CSSSanitizer

def sanitize_markdown(markdown_content):
    # Define allowed tags for sanitization
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [
        'p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'br', 'pre', 'code', 'img', 'blockquote',
    ]

    # Define allowed attributes
    allowed_attributes = dict(bleach.sanitizer.ALLOWED_ATTRIBUTES)
    allowed_attributes.update({
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title'],
        '*': ['class', 'style'],  # Allow "style" for all elements
    })

    # Define allowed CSS properties if style attributes are used
    css_sanitizer = CSSSanitizer(
        allowed_css_properties=[
            'color', 'font-size', 'font-weight', 'font-style',  # Add more if needed
            'text-decoration', 'background-color', 'border',
            'margin', 'padding', 'display', 'width', 'height',
        ]
    )

    # Convert Markdown to HTML
    html_content = markdown(
        markdown_content, extensions=settings.MARKDOWNX_MARKDOWN_EXTENSIONS
    )

    # Sanitize HTML content
    cleaned_content = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        css_sanitizer=css_sanitizer,  # Use CSS sanitizer explicitly
        strip=True,
    )
    return cleaned_content
