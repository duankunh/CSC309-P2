from rest_framework import serializers
from .models import Calendar, Meeting, Preference, Schedule


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'name', 'date', 'duration', 'calendar']


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['id', 'start_time', 'end_time', 'preference_level', 'meeting', 'contact', 'status']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'start_time', 'end_time', 'schedule_status', 'meeting']




