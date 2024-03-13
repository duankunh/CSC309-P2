from django.db import models
from django.conf import settings
# from scheduler.models import Meeting
class Contact(models.Model):
    STATUS_CHOICES = [
        ('None', 'None'),
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES,
                              default='None')
    # meetings = models.ManyToManyField(Meeting, related_name='contacts')

    class Meta:
        app_label = 'contacts'
