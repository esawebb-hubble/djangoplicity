# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>


from django.utils.translation import ugettext_noop
from djangoplicity.archives.resources import FileType


class LegacyVideo(FileType):
    verbose_name = ugettext_noop(u'Legacy Video')
    exts = ['m4v', 'flv', 'mov', 'avi', 'mpeg', 'mp4', 'mpg', 'mp2', 'gif' ]
    content_type = 'video/*'


class VodcastType(FileType):
    verbose_name = ugettext_noop(u'Video Podcast')
    exts = ['m4v', 'm4v']


class FlvType(FileType):
    verbose_name = ugettext_noop(u'Flash Video')
    exts = ['flv']


class SwfType(FileType):
    verbose_name = ugettext_noop(u'Flash')
    exts = ['swf']


class HD720PType(FileType):
    verbose_name = ugettext_noop(u'HD 720p')
    exts = ['m4v', 'mp4']


class HD1080PType(FileType):
    verbose_name = ugettext_noop(u'HD 1080p')
    exts = ['mp4', 'm4v']


class H264Type(FileType):
    verbose_name = ugettext_noop(u'H.264 MPEG-4')
    exts = ['mp4', 'm4v']


class M4VType(FileType):
    verbose_name = ugettext_noop(u'M4V')
    exts = ['m4v']


class MP4Type(FileType):
    verbose_name = ugettext_noop(u'MP4')
    exts = ['mp4']


class MpegType(FileType):
    verbose_name = ugettext_noop(u'MPEG')
    exts = ['mpg', 'mpeg']


class MovType(FileType):
    verbose_name = ugettext_noop(u'Quicktime')
    exts = ['mov']


class BroadcastType(FileType):
    verbose_name = ugettext_noop('Broadcast')
    exts = ['avi', 'mxf', 'm2t', 'mov']


class HDAndAppleType(M4VType):
    width = 1280
    height = 720


class DomeMovType(FileType):
    verbose_name = ugettext_noop(u'Fulldome 1.5k mov')
    exts = ['mov', 'mp4']
    width = 1536
    height = 1536


class Dome2kMasterType(FileType):
    verbose_name = ugettext_noop(u'Fulldome 2k Master')
    exts = ['avi', 'zip']
    width = 2048
    height = 2048


class Dome4kMasterType(FileType):
    verbose_name = ugettext_noop(u'Fulldome 4k Master')
    exts = ['avi', 'zip']
    width = 4096
    height = 4096


class Dome8kMasterType(FileType):
    verbose_name = ugettext_noop(u'Fulldome 8k Master')
    exts = ['avi', 'zip']
    width = 8192
    height = 8192


class MediumPodcastType(FileType):
    verbose_name = ugettext_noop(u'Video Podcast')
    exts = ['m4v', 'mp4']


class DomePreviewType(FileType):
    verbose_name = ugettext_noop(u'Fulldome Preview')
    exts = ['mp4']
    width = 1024
    height = 1024


class VR8kType(FileType):
    verbose_name = ugettext_noop(u'8k VR')
    exts = ['mp4']
    width = 4096
    height = 2048


class VR4kType(FileType):
    verbose_name = ugettext_noop(u'4k VR')
    exts = ['mp4']
    width = 8192
    height = 4096

class VR4kMasterType(FileType):
    verbose_name = ugettext_noop(u'4k Master VR')
    exts = ['mov']
    width = 4096
    height = 2048

class VR8kMasterType(FileType):
    verbose_name = ugettext_noop(u'8k Master VR')
    exts = ['avi', 'zip']
    width = 8192
    height = 4096

class VR16kMasterType(FileType):
    verbose_name = ugettext_noop(u'16k Master VR')
    exts = ['avi', 'zip']
    width = 16384
    height = 8192


class CylindricalPreviewType(FileType):
    verbose_name = ugettext_noop(u'Cylindrical VR Preview')
    exts = ['mp4']


class Cylindrical4kMasterType(FileType):
    verbose_name = ugettext_noop(u'4k Cylindrical VR Master')
    exts = ['zip']


class Cylindrical8kMasterType(FileType):
    verbose_name = ugettext_noop(u'8k Cylindrical VR Master')
    exts = ['zip']


class Cylindrical16kMasterType(FileType):
    verbose_name = ugettext_noop(u'16k Cylindrical VR Master')
    exts = ['zip']


class UltraHDType(FileType):
    verbose_name = ugettext_noop(u'Ultra HD (4k/2160p)')
    exts = ['mp4']
    width = 3840
    height = 2160
    bitrate = 30000

class FullHDPreview1080p(MP4Type):
    width = 1920
    height = 1080
    bitrate = 30000

class UltraHDH265Type(FileType):
    verbose_name = ugettext_noop(u'Ultra HD (4k/2160p)')
    exts = ['mkv', 'mp4']


class UltraHDBroadcastType(FileType):
    verbose_name = ugettext_noop(u'Ultra HD Broadcast (4k/2160p)')
    exts = ['avi', 'mov']


class BroadcastSDType(FileType):
    verbose_name = ugettext_noop(u'Brodcast SD')
    exts = ['mxf', 'avi', 'mov']  # mov to be removed


class SubtitleType (FileType):
    verbose_name = ugettext_noop(u'Subtitle')
    exts = ['srt']


class AudioTrackType (FileType):
    verbose_name = ugettext_noop(u'Audio Track')
    exts = ['zip', 'wav']

class QHDPreviewType(FileType):
    name = "qhd_1440p25_screen"
    label = "2.5K QHD Preview"
    extension = "mp4"
    mime_type = "video/mp4"
    codec = "MPEG4 H.264"
    width = 2560
    height = 1440
    frame_rate = 25
    bitrate = 14000

class K8PreviewType(FileType):
    name = "8k_4320p25_screen"
    label = "8K Preview"
    extension = "mp4"
    mime_type = "video/mp4"
    codec = "MPEG4 H.264"
    width = 7680
    height = 4320
    frame_rate = 25
    bitrate = 90000

class MobileFullHDPreviewType(FileType):
    name = "m_hd_1080p_screen"
    label = "Mobile 1080P Full HD Preview"
    extension = "mp4"
    mime_type = "video/mp4"
    codec = "MPEG4 H.264"
    width = 1080
    height = 1920
    frame_rate = 30
    bitrate = 12000

class MobileUltraHDPreviewType(FileType):
    name = "m_ultra_hd_screen"
    label = "Mobile 4K Ultra HD Preview"
    extension = "mp4"
    mime_type = "video/mp4"
    codec = "MPEG4 H.264"
    width = 2160
    height = 3840
    frame_rate = 30
    bitrate = 36000
