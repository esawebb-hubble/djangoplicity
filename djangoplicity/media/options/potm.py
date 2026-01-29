from builtins import object
from django.utils.translation import ugettext_noop
from djangoplicity.archives.contrib.browsers import ListBrowser, SerializationBrowser
from djangoplicity.archives.contrib.queries import EmbargoQuery, StagingQuery, YearQuery
from djangoplicity.archives.contrib.serialization.serializers import JSONEmitter, ICalEmitter
from djangoplicity.archives.contrib.templater import DisplayTemplate
from djangoplicity.archives.options import ArchiveOptions
from djangoplicity.archives.views import SerializationDetailView

from djangoplicity.media.queries import PotmAllPublicQuery
from djangoplicity.media.serializers import (
    PictureOfTheMonthSerializer,
    ICalPictureOfTheMonthSerializer,
)


class PictureOfTheMonthOptions(ArchiveOptions):
    urlname_prefix = "potm"

    detail_views = (
        {
            'url_pattern': 'api/(?P<serializer>json)/',
            'view': SerializationDetailView(
                serializer=PictureOfTheMonthSerializer,
                emitters=[JSONEmitter],
            ),
            'urlname_suffix': 'serialization',
        },
    )

    search_fields = (
        'image__id', 'image__title', 'image__headline', 'image__description',
        'image__subject_name__name', 'image__subject_name__alias',
        'image__credit', 'image__type',
        'video__id', 'video__title', 'video__headline', 'video__description',
        'video__subject_name__name', 'video__subject_name__alias',
        'video__facility__name', 'video__credit', 'video__type',
    )

    class Queries(object):
        default = PotmAllPublicQuery(
            browsers=('normal', 'viewall', 'json', 'ical'),
            verbose_name=ugettext_noop('Picture of the Month'),
            feed_name="default",
        )
        embargo = EmbargoQuery(
            browsers=('normal', 'viewall', 'json', 'ical'),
            verbose_name=ugettext_noop('Picture of the Month (embargoed)'),
        )
        staging = StagingQuery(
            browsers=('normal', 'viewall', 'json', 'ical'),
            verbose_name=ugettext_noop('Picture of the Month (staging)'),
        )
        year = YearQuery(
            browsers=('normal', 'viewall', 'json', 'ical'),
            verbose_name=ugettext_noop('Picture of the Month %d'),
            feed_name="default",
        )

    class Browsers(object):
        normal = ListBrowser(paginate_by=20)
        viewall = ListBrowser(paginate_by=100)
        json = SerializationBrowser(
            serializer=PictureOfTheMonthSerializer,
            emitter=JSONEmitter,
            paginate_by=20,
            display=False,
            verbose_name=ugettext_noop("JSON"),
        )
        ical = SerializationBrowser(
            serializer=ICalPictureOfTheMonthSerializer,
            emitter=ICalEmitter,
            paginate_by=100,
            display=False,
            verbose_name=ugettext_noop("iCal"),
        )

    class Display(object):
        multiple_potm = DisplayTemplate(
            'template',
            "{%block org_prefix %}ESO{% endblock %} "
            "Picture of the Month: {{obj.image.title}}<br/>"
            "<a href=\"{{site_url_prefix}}{{obj.get_absolute_url}}\">"
            "{{site_url_prefix}}{{obj.get_absolute_url}}</a>",
            name='Multiple POTM list',
        )

        multiple_potm_text = DisplayTemplate(
            'template',
            "{%block org_prefix %}ESO{% endblock %} "
            "Picture of the Month: {{obj.image.title}}<br/>"
            "{{site_url_prefix}}{{obj.get_absolute_url}}",
            name='Multiple POTM list (plaintext)',
        )

        potm_available_announcement = DisplayTemplate(
            'file',
            'archives/pictureofthemonth/email/translations_available_potm.html',
            name='Picture of the Month available for translation',
        )

    @staticmethod
    def feeds():
        from djangoplicity.media.feeds import PictureOfTheMonthFeed
        return {
            '': PictureOfTheMonthFeed,
        }
