from ces.models import TipoObjeto

from django import template
register = template.Library()


@register.inclusion_tag('ces/categories.html')
def show_categories(current_tipo_id=None):
    categories = TipoObjeto.objects.all()
    return {'categories': categories, 'current_tipo_id': current_tipo_id}
