from django.contrib import admin
from .models import Calendar, Meeting, Preference

admin.site.register(Calendar)
admin.site.register(Meeting)
admin.site.register(Preference)

# Register your models here.
