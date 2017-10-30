# coding=utf-8
from django import template
register = template.Library()


@register.filter()
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter()
def human_readable(value, arg):
    if hasattr(value, 'get_' + str(arg) + '_display'):
        return getattr(value, 'get_%s_display' % arg)()
    elif hasattr(value, str(arg)):
        if callable(getattr(value, str(arg))):
            return getattr(value, arg)()
        else:
            return getattr(value, arg)
    else:
        try:
            return value[arg]
        except KeyError:
            return settings.TEMPLATE_STRING_IF_INVALID
