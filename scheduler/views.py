from django.http import JsonResponse
from django.shortcuts import render
from .models import Calendar, Meeting, Preference, Schedule
from .serializers import CalendarSerializer, MeetingSerializer, PreferenceSerializer, ScheduleSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from datetime import timedelta, datetime, date



@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def calendar(request):

    if request.method == 'GET':
        calendars = Calendar.objects.filter(owner=request.user)
        serializer = CalendarSerializer(calendars, many=True)
        return JsonResponse({'calendars': serializer.data})

    if request.method == 'POST':
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def meeting(request, id):
    try:
        Calendar.objects.get(pk=id)
    except Calendar.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        meetings = Meeting.objects.filter(calendar=id)  # Get all meeting under <id> calendar
        serializer = MeetingSerializer(meetings, many=True)
        return JsonResponse({'meetings': serializer.data})

    if request.method == 'POST':
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def preference(request, id):
    try:
        Meeting.objects.get(pk=id)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        preference = Preference.objects.filter(meeting=id) # Get all preference under <id> meeting
        serializer = PreferenceSerializer(preference, many=True)
        return JsonResponse({'preference': serializer.data})

    if request.method == 'POST':
        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def schedule_proposals(request, id):
    try:
        Meeting.objects.get(pk=id)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        schedule = Schedule.objects.filter(meeting=id) # Get all schedules under <id> meeting
        serializer = ScheduleSerializer(schedule, many=True)
        return JsonResponse({'preference': serializer.data})

    if request.method == 'POST':
        serializer = ScheduleSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def schedule_get_finalize(request, id):
    try:
        Meeting.objects.get(pk=id)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        schedule = Schedule.objects.filter(meeting=id, schedule_status='finalized') # Get finalized schedule under <id> meeting
        serializer = ScheduleSerializer(schedule, many=True)
        return JsonResponse({'preference': serializer.data})

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def schedule_make_finalize(request, meeting_id, schedule_id):
    try:
        Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        schedule = Schedule.objects.get(pk=schedule_id) # Get <shcedule_id> schedules under <id> meeting
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def preference_update(request, meeting_id, preference_id):
    try:
        Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        preference = Preference.objects.get(pk=preference_id)
    except Preference.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PreferenceSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for testing the implementation of suggested schedule
####################
####################
