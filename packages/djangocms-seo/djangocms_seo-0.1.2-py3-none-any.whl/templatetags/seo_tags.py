from django import template
from djangocms_seo.models import SeoExtension

register = template.Library()

@register.simple_tag(takes_context=True)
def seo_meta_tags(context):
    request = context['request']
    page = request.current_page
    if page:
        try:
            seo_extension = SeoExtension.objects.get(extended_object=page)
            return seo_extension.get_seo_html()
        except SeoExtension.DoesNotExist:
            return ''
    return ''