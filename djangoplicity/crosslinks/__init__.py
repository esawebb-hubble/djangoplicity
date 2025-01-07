"""
Simple module for defining cross-links between archives on ESO-hosted djangoplicity sites.
"""
from django.conf import settings

url = settings.SITE_DOMAIN
domain = url.split(".", 1)[1] if url.startswith("www.") else url

_ = lambda x: x

ARCHIVE_CROSSLINKS = {
    'announcements': (
        (domain, f'https://{domain}/announcements/'),
    ),
    'releases': (
        (domain, f'https://{domain}/news/'),
    ),
    'images': (
        (domain, f'https://{domain}/images/'),
    ),
    'videos': (
        (domain, f'https://{domain}/videos/'),
    ),
    'potw': (
        (domain, f'https://{domain}/images/potm/'),
    ),
    'posters': (
        (domain, f'https://{domain}/products/print_posters/'),
    ),
    'books': (
        (domain, f'https://{domain}/about/further_information/books/'),
    ),
    'brochures': (
        (domain, f'https://{domain}/about/further_information/brochures/'),
    ),
    'calendars': (
        (domain, f'https://{domain}/products/calendars/'),
    ),
    'education': (
        #(domain, f'https://{domain}/projects/anniversary/educational_material/'),
    ),
    'newsletters': (
        (domain, f'https://{domain}/newsletters/'),

    ),
    'periodicals': (
        # ( domain, f'https://{domain}/about/further_information/newsletters/' )#brokend
    ),
    'postcards': (
        (domain, f'https://{domain}/products/postcards/'),
    ),
    'logos': (
        (domain, f'https://{domain}/products/logos/'),
    ),
    'conferenceposters': (
        (domain, f'https://{domain}/products/conf_posters/'),
    ),
    'presentations': (
        (domain, f'https://{domain}/products/presentations/'),
    ),
    'exhibitions': (
        (domain, f'https://{domain}/products/exhibitions/'),
    ),
    'dvds': (
        (domain, f'https://{domain}/products/media/'),
    ),
    'techdocs': (
        # ( domain, 'http://{domain}/about/further_information/techdocs/' )#roto
    ),

}


STRINGS = (
    _('Also see our images on %(websites)s'),
    _('Also see our videos on %(websites)s'),
    _('Also see our press releases on %(websites)s'),
    _('Also see our technical documents on %(websites)s'),
    _('Also see our exhibitions on %(websites)s'),
    _('Also see our announcements on %(websites)s'),
    _('Also see our postcards on %(websites)s'),
    _('Also see our books on %(websites)s'),
    _('Also see our brochures on %(websites)s'),
    _('Also see our dvds on %(websites)s'),
    _('Also see our newsletters on %(websites)s'),
    _('Also see our posters on %(websites)s'),
    _('Also see our pictures of the week on %(websites)s'),
    _('Also see our calendars on %(websites)s'),
    _('Also see our conference posters on %(websites)s'),

    _('images on %(websites)s'),
    _('videos on %(websites)s'),
    _('press releases on %(websites)s'),
    _('technical documents on %(websites)s'),
    _('exhibitions on %(websites)s'),
    _('announcements on %(websites)s'),
    _('postcards on %(websites)s'),
    _('books on %(websites)s'),
    _('brochures on %(websites)s'),
    _('dvds on %(websites)s'),
    _('newsletters on %(websites)s'),
    _('posters on %(websites)s'),
    _('pictures of the week on %(websites)s'),
    _('calendars on %(websites)s'),
    _('conference posters on %(websites)s'),
)


def crosslinks_for_domain( domain ):
    tmp = {}

    for key, values in list(ARCHIVE_CROSSLINKS.items()):
        tmp[key] = [d_u for d_u in values if d_u[0] != domain]

    return tmp
