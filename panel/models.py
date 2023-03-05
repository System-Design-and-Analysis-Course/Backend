from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import Customer

VIDEO = 'Video'
AUDIO = 'Audio'
BOOK = 'Book'

CONTENTTYPE_CHOICES = (
    (VIDEO, _('Video')),
    (AUDIO, _('Audio')),
    (BOOK, _('Book')),
)


class CustomDate(models.Model):
    created_at = models.DateTimeField(_("date created"), default=timezone.now)
    last_modified_at = models.DateTimeField(_("date modified"), default=timezone.now)


class Library(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.CharField(
        max_length=10, choices=CONTENTTYPE_CHOICES, default=BOOK,
        verbose_name=_('ContentType'),
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_info = models.ForeignKey(CustomDate, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'content_type', 'user',)


class File(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.CharField(
        max_length=10, choices=CONTENTTYPE_CHOICES, default=BOOK,
        verbose_name=_('ContentType'),
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_info = models.ForeignKey(CustomDate, on_delete=models.PROTECT, null=True, blank=True)
    libraries = models.ManyToManyField(Library)
    content = models.FileField(upload_to='static/')

    class Meta:
        unique_together = ('name', 'content_type', 'user',)


class Attachment(models.Model):
    name = models.CharField(max_length=50)
    date_info = models.ForeignKey(CustomDate, on_delete=models.PROTECT, null=True, blank=True)
    content = models.FileField(null=True, blank=True, upload_to='static/')
    value = models.TextField(max_length=500, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('file', 'name',)


class SharedFile(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_files')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_files')
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sender', 'receiver', 'file',)
