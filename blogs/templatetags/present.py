from django import template

import markdown
import bleach


register = template.Library()


def present(value, arg):
    tags = bleach.ALLOWED_TAGS.extend(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'cite', 'img'])
    attributes = bleach.ALLOWED_ATTRIBUTES
    attributes['img'] = ['src']
    styles = bleach.ALLOWED_STYLES
    return bleach.clean(markdown.markdown(value), tags=tags, attributes=attributes, styles=styles, strip=False, strip_comments=True)