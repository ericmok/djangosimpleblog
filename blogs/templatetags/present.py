from django import template

import markdown
import bleach


register = template.Library()


def inner_present(value):
    bleach.ALLOWED_TAGS.extend(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'cite', 'img', 'p'])
    bleach.ALLOWED_ATTRIBUTES['img'] = ['src']
    markdown_text = markdown.markdown(value)
    return bleach.clean(markdown_text, strip=False, strip_comments=True)


@register.filter
def present(value):
    inner_present(value)