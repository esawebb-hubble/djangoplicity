# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>

from django.conf import settings
from django.db.models import Q
from django.http import Http404
from djangoplicity.archives.contrib.queries import CategoryQuery
from djangoplicity.metadata.models import Category

if settings.USE_I18N:
    from djangoplicity.translation.models import TranslationModel


class WebCategoryQuery(CategoryQuery):

    def __init__(self, category_type=None, **kwargs):
        self.category_type = category_type
        self.use_category_title = False
        defaults = {'searchable': True}
        defaults.update( kwargs )
        super(WebCategoryQuery, self).__init__( **defaults )

    def queryset(self, model, options, request, stringparam=None, **kwargs):
        if not stringparam:
            raise Http404

        try:
            category = Category.objects.get(url=stringparam, type__name=self.category_type)
        except Category.DoesNotExist:
            # URL of non existing category specified.
            raise Http404

        params = {
            self.relation_field: category,
        }

        q_obj = Q(**params)

        # hack: added source if model has source attr so that translation lookups work
        if settings.USE_I18N and issubclass( model, TranslationModel ):
            params2 = {}
            for k in list(params.keys()):
                params2['source__' + k] = params[k]
            q_obj = q_obj | Q(**params2)

        # We want to call the queryset from the parent of CategoryQuery and not
        # of WebCategoryQuery
        # pylint: disable=E1003
        (qs, _query_data) = super(CategoryQuery, self).queryset(model, options, request, **kwargs)
        qs = qs.filter(q_obj)
        return (qs, {'category': category})

    def verbose_name(self, category=None, **kwargs ):
        if category and self.use_category_title:
            return self._verbose_name % { 'title': category.name }
        else:
            return self._verbose_name
