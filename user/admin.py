from django.contrib import admin

from user.models import Customer
from panel.models import CustomDate, Attachment, File, SharedFile, Library

# Register your models here.

admin.site.register(Customer)
admin.site.register(CustomDate)
admin.site.register(Library)
admin.site.register(Attachment)
admin.site.register(File)
admin.site.register(SharedFile)
