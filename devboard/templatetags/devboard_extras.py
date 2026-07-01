from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def status_badge(task):
    colors = {
        "TODO": "#6c757d",
        "IN_PROGRESS": "#0d6efd",
        "DONE": "#198754",
    }
    icons = {
        "TODO": "circle",
        "IN_PROGRESS": "spinner",
        "DONE": "check-circle",
    }
    color = colors.get(task.status, "#000")
    return format_html(
        '<span style="background:{};color:white;padding:2px 8px;border-radius:4px">{}</span>',
        color, task.get_status_display(),
    )