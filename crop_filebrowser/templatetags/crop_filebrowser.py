from django.template import Library, TemplateSyntaxError

from filebrowser.templatetags.fb_versions import VersionNode
from filebrowser.settings import VERSIONS

register = Library()


class VersionObjectThumbnailNode(VersionNode):
    def render(self, context):
        result = super(VersionObjectThumbnailNode, self).render(context)
        if not context[self.var_name]:
            return ""
        version_suffix = self.suffix.resolve(context)
        version = VERSIONS[version_suffix]
        obj = context[self.var_name]
        obj.version_dimensions = '%sx%s' % (version['width'],
                                            version['height'])
        context[self.var_name] = obj
        return result


@register.tag
def version_object_thumbnail(parser, token):
    """
    Returns a context variable 'var_name' with the FileObject
    {% version_object fileobject version_suffix as var_name %}

    Use {% version_object fileobject 'medium' as version_medium %} in order to
    retrieve the medium version of an image stored in a variable version
    medium. version_suffix can be a string or a variable. If version_suffix is
    a string, use quotes.
    """

    bits = token.split_contents()
    if len(bits) != 5:
        raise TemplateSyntaxError("'version_object' tag takes 4 arguments")
    if bits[3] != 'as':
        raise TemplateSyntaxError(
            "second argument to 'version_object' tag must be 'as'")
    return VersionObjectThumbnailNode(parser.compile_filter(bits[1]),
                                      parser.compile_filter(bits[2]), bits[4])
