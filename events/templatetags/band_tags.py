from events.models import searchBandSugg
from django import template

register = template.Library()


@register.simple_tag
def is_in_note(x):
     return searchBandSugg.objects.filter(name__in=x.notes.split()).exists()