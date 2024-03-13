from django.db import models
from django.conf import settings
class Calendar(models.Model):
    name = models.CharField(max_length=100)  # Name of the calendar
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendars')
    # description = models.TextField()

    def __str__(self):
        return self.name

class Meeting(models.Model):
    name = models.CharField(max_length=200)  # Name of the meeting
    date = models.DateField()  # Date of the meeting
    duration = models.DurationField()  # Duration of the meeting
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Preference(models.Model):
    start_time = models.TimeField()  # Start time of non-busy time
    end_time = models.TimeField()  # End time of the non-busy time
    preference_choices = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    preference_level = models.CharField(
        max_length=10,
        choices=preference_choices,
        default='medium',  # Set default preference level to medium
    )
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return self.meeting.name + ' Preference' +str(self.id)

class Schedule(models.Model):
    start_time = models.TimeField()  # Start time of schedule
    end_time = models.TimeField()  # End time of schedule
    schedule_type = [
        ('finalized', 'Finalized'),
        ('undecided', 'Undecided'),
    ]
    schedule_status = models.CharField(
        max_length=10,
        choices=schedule_type,
        default='undecided',  # Set default preference level to medium
    )
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return self.meeting.name + ' Schedule' +str(self.id)
# Create your models here.
