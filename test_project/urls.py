"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions
from djangoplicity.media.models import Image, Video, PictureOfTheWeek, ImageComparison
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions, ImageComparisonOptions
from djangoplicity.announcements.models import Announcement, WebUpdate
from djangoplicity.announcements.options import AnnouncementOptions, WebUpdateOptions
from test_project.admin import admin_site, adminlogs_site

import django
if django.VERSION >= (2, 0):
    from django.contrib.auth.views import LoginView as login
else:
    from django.contrib.auth.views import login

urlpatterns = [
    # Djangoplicity Administration
    url(r'^admin/', admin_site.urls, {'extra_context': {'ADMIN_SITE': True}}),
    url(r'^admin/cache/', include(('djangoplicity.cache.urls', 'cache'), namespace='admincache_site')),
    url(r'^admin/history/', include(('djangoplicity.adminhistory.urls', 'history'), namespace='adminhistory_site')),
    url(r'^admin/system/', adminlogs_site.urls, {'extra_context': {'ADMINLOGS_SITE': True}}),
    url(r'^admin/', include('djangoplicity.metadata.wtmlimport.urls'), {'extra_context': {'ADMIN_SITE': True}}),
    url(r'^admin/import/', include('djangoplicity.archives.importer.urls')),
    url(r'^tinymce/', include('tinymce.urls')),

    # Media Archive (Order of the URLs is important because they have common subpaths)
    url(r'^news/', include('djangoplicity.releases.urls'), {'model': Release, 'options': ReleaseOptions, 'translate': True}),
    url(r'^images/iotw/', include('djangoplicity.media.urls_potw'), {'model': PictureOfTheWeek, 'options': PictureOfTheWeekOptions, 'translate': True}),
    url(r'^images/comparisons/', include('djangoplicity.media.urls_imagecomparisons'), {'model': ImageComparison, 'options': ImageComparisonOptions, 'translate': True}),
    url(r'^images/', include('djangoplicity.media.urls_images'), {'model': Image, 'options': ImageOptions, 'translate': True}),
    url(r'^videos/', include('djangoplicity.media.urls_videos'), {'model': Video, 'options': VideoOptions, 'translate': True}),

    # Apps
    url(r'^reports/', include('djangoplicity.reports.urls')),

    # Other archives
    url( r'^announcements/webupdates/', include('djangoplicity.announcements.urls_webupdates'), { 'model': WebUpdate, 'options': WebUpdateOptions } ),
    url( r'^announcements/', include('djangoplicity.announcements.urls'), { 'model': Announcement, 'options': AnnouncementOptions } ),

    # User Auth
    url( r'^login/$', login, { 'template_name': 'login.html' } ),

    # ETC
    url(r'^eventcalendar/', include('djangoplicity.eventcalendar.urls')),
    url( r'^facebook/', include('djangoplicity.iframe.urls')  ),
]

# This only works if DEBUG=True
if settings.SERVE_STATIC_MEDIA:
   from django.conf.urls.static import static
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
