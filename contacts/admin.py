from django.contrib import admin
from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status',
                    'owner')
    search_fields = ('name', 'email')
    list_filter = ('status', 'owner')
