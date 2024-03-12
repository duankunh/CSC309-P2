from django.db import models

class Calendar(models.Model):
    name = models.CharField(max_length=100)  # Name of the calendar
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
# Create your models here.
