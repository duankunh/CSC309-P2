from rest_framework import serializers
from .models import Calendar, Meeting, Preference
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'name']

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'name', 'date', 'duration', 'calendar']

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['id', 'start_time', 'end_time', 'preference_level', 'meeting']