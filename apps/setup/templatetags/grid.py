from django import template

register = template.Library()

@register.filter(name='grid_size')
def grid_size(field):
    return field.field.widget.attrs.get('grid_size', 'w-full')
