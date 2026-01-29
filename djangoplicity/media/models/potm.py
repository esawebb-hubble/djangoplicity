from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from djangoplicity.archives import fields as archive_fields
from djangoplicity.archives.base import ArchiveModel
from djangoplicity.archives.translation import TranslationProxyMixin
from djangoplicity.archives.utils import (
    propagate_release_date,
    release_date_change_check,
)

from djangoplicity.media.models.comparisons import (
    ImageComparison,
    ImageComparisonProxy,
)
from djangoplicity.media.models.images import Image, ImageProxy
from djangoplicity.media.models.videos import Video, VideoProxy
from djangoplicity.translation.models import (
    TranslationForeignKey,
    TranslationModel,
)


# Picture of the Month
# ====================

@python_2_unicode_compatible
class PictureOfTheMonth(ArchiveModel, TranslationModel):
    """
    Model representing a Picture of the Month.
    The model can either use an image, a video or an image comparison
    as its main visual. The release date set will be propagated to the
    related object.
    """
    id = archive_fields.IdField()
    image = TranslationForeignKey(
        Image, blank=True, null=True, only_sources=False, on_delete=models.CASCADE
    )
    video = TranslationForeignKey(
        Video, blank=True, null=True, only_sources=False, on_delete=models.CASCADE
    )
    comparison = models.ForeignKey(
        ImageComparison, blank=True, null=True, on_delete=models.CASCADE
    )
    auto_update = True

    def visual(self):
        """
        Obtain either an image, a video or a comparison if specified.
        """
        if self.image:
            return self.image
        elif self.video:
            return self.video
        elif self.comparison:
            return self.comparison
        return None

    def get_absolute_url(self):
        """
        URL of image or video detail view, since POTM does not
        use its own detail view.
        """
        v = self.visual()
        return v.get_absolute_url() if v else None

    def rename(self, new_pk):
        """
        Extend Archive's rename() to send email notification if original is renamed
        """
        pot_name = 'Pictures of the Month'
        pot_tag = 'POTM_RENAME_NOTIFY'

        if self.published and self.is_source() and hasattr(settings, 'RELEASE_RENAME_NOTIFY'):
            msg_subject = '%s renamed: %s -> %s' % (pot_name, self.pk, new_pk)
            msg_body = """https://www.eso.org/public/images/%s/""" % new_pk
            msg_from = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
            msg_to = getattr(settings, pot_tag, '')
            if msg_from and msg_to:
                send_mail(msg_subject, msg_body, msg_from, msg_to, fail_silently=False)

        return super(PictureOfTheMonth, self).rename(new_pk)

    def save(self, **kwargs):
        signals.post_save.disconnect(PictureOfTheMonth.post_save_handler, sender=PictureOfTheMonth)
        signals.post_save.disconnect(PictureOfTheMonth.post_related_save_handler, sender=Image)
        signals.post_save.disconnect(PictureOfTheMonth.post_related_save_handler, sender=ImageProxy)
        signals.post_save.disconnect(PictureOfTheMonth.post_related_save_handler, sender=Video)
        signals.post_save.disconnect(PictureOfTheMonth.post_related_save_handler, sender=VideoProxy)
        signals.post_save.disconnect(PictureOfTheMonth.post_related_save_handler, sender=ImageComparison)
        signals.post_save.disconnect(PictureOfTheMonth.post_related_save_handler, sender=ImageComparisonProxy)

        super(PictureOfTheMonth, self).save(**kwargs)

        signals.post_save.connect(PictureOfTheMonth.post_save_handler, sender=PictureOfTheMonth)
        signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=Image)
        signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=ImageProxy)
        signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=Video)
        signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=VideoProxy)
        signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=ImageComparison)
        signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=ImageComparisonProxy)

    @classmethod
    def get_latest(cls):
        """
        Method to get the latest public POTM
        """
        try:
            now = datetime.now()
            return cls.objects.filter(
                published=True,
                release_date__lt=now,
                embargo_date__lt=now,
            ).order_by('-release_date')[0]
        except IndexError:
            raise cls.DoesNotExist

    def __str__(self):
        v = self.visual()
        return "%s - %s" % (self.id, v.title) if v else self.id

    @classmethod
    def post_save_handler(cls, sender, instance=None, created=False, raw=False, **kwargs):
        """
        Automatically create/delete POTM translations for images/videos/comparisons.
        """
        if instance.auto_update and not raw:
            # Delete all translations and add new ones
            instance.translations.all().delete()
            for attr in ['image', 'comparison', 'video']:
                # If related object exists and has translations, then
                # create corresponding potw translations for all.
                related_object = getattr(instance, attr)
                if related_object and isinstance(related_object, TranslationModel):
                    for related_obj_trans in related_object.translations.all():
                        potm_trans = PictureOfTheMonthProxy(**{
                            attr: related_obj_trans,
                            'lang': related_obj_trans.lang,
                            'source': instance,
                            'translation_ready': related_obj_trans.translation_ready,
                            'published': related_obj_trans.published,
                        })
                        potm_trans.clean()
                        potm_trans.save()
                    break

    @classmethod
    def post_related_save_handler(cls, sender, instance=None, created=False, raw=False, **kwargs):
        """
        Once a related object is saved, we might need to run post_save_handler for the POTM
        """
        if not raw and isinstance(instance, TranslationModel):
            instance = instance if instance.is_source() else instance.source
            for potm in instance.pictureofthemonth_set.all():
                cls.post_save_handler(sender, instance=potm, created=created, raw=raw)

    class Meta:
        ordering = ('-release_date',)
        verbose_name_plural = _('Pictures of the Month')
        app_label = 'media'
        permissions = [
            ("view_only_non_default", "Can view only non default language"),
        ]

    class Translation:
        fields = ['image', 'video', 'comparison']
        excludes = ['published', 'last_modified', 'created']

    class Archive:
        class Meta:
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True
            rename_pk = ('media_pictureofthemonth', 'id')
            rename_fks = (
                ('media_pictureofthemonth', 'source_id'),
                ('media_image', 'release_date_owner'),
                ('media_video', 'release_date_owner'),
                ('media_imagecomparison', 'release_date_owner'),
            )
            sort_fields = ['last_modified', 'release_date']


# ========================================================================
# Translation proxy model
# ========================================================================

class PictureOfTheMonthProxy(PictureOfTheMonth, TranslationProxyMixin):
    """
    Translation proxy model for Picture of the Month.
    """
    objects = PictureOfTheMonth.translation_objects

    def clean(self):
        # Note: For some reason it's not possible to
        # to define clean/validate_unique in TranslationProxyMixin
        # so we have to do this trick, where we add the methods and
        # call into translation proxy mixin.
        self.id_clean()

    def validate_unique(self, exclude=None):
        self.id_validate_unique(exclude=exclude)

    class Meta:
        proxy = True
        verbose_name = _('Pictures of the Month translation')
        app_label = 'media'

    class Archive:
        class Meta:
            rename_pk = ('media_pictureofthemonth', 'id')
            rename_fks = (
                ('media_pictureofthemonth', 'source_id'),
                ('media_image', 'release_date_owner'),
                ('media_video', 'release_date_owner'),
                ('media_imagecomparison', 'release_date_owner'),
            )


# Signals
signals.pre_save.connect(release_date_change_check, sender=PictureOfTheMonth)
signals.pre_save.connect(release_date_change_check, sender=PictureOfTheMonthProxy)
signals.post_save.connect(PictureOfTheMonth.post_save_handler, sender=PictureOfTheMonth)
signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=Image)
signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=ImageProxy)
signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=Video)
signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=VideoProxy)
signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=ImageComparison)
signals.post_save.connect(PictureOfTheMonth.post_related_save_handler, sender=ImageComparisonProxy)

# Propagate PictureOfTheMonth release date to Image, Video and Comparison
propagate_release_date(PictureOfTheMonth.image)
propagate_release_date(PictureOfTheMonth.video)
propagate_release_date(PictureOfTheMonth.comparison)