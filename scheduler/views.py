from django.http import JsonResponse
from django.shortcuts import render
from scheduler.models import Calendar, Meeting, Preference
from scheduler.serializers import CalendarSerializer, MeetingSerializer, PreferenceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def calendar_all(request):

    if request.method == 'GET':
        calendars = Calendar.objects.all()
        serializer = CalendarSerializer(calendars, many=True)
        return JsonResponse({'calendars': serializer.data})

    if request.method == 'POST':
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def meeting_all(request, id):
    try:
        Calendar.objects.get(pk=id)
    except Calendar.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        meetings = Meeting.objects.filter(calendar=id)
        serializer = MeetingSerializer(meetings, many=True)
        return JsonResponse({'meetings': serializer.data})

    if request.method == 'POST':
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def preference_all(request, id):
    try:
        Meeting.objects.get(pk=id)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        preference = Preference.objects.filter(meeting=id)
        serializer = PreferenceSerializer(preference, many=True)
        return JsonResponse({'preference': serializer.data})

    if request.method == 'POST':
        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
# Create your views here.
