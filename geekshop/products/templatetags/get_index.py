from django import template

register = template.Library()


@register.filter(name='get_index')
def get_index(obj_to_index, i):
    return obj_to_index.index(i)
