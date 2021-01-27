from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)


def reverse_text(text: str) -> str:
    return text[::-1]


register.filter('reverse_text', reverse_text)
