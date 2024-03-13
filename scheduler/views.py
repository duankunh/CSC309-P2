from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Calendar, Meeting, Preference, Schedule, Contact
from .serializers import CalendarSerializer, MeetingSerializer, PreferenceSerializer, ScheduleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Calendar
import json
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Contact
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def calendar(request):

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
# Create your views here.



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modify_non_busy_times(request):
    try:
        data = json.loads(request.body)
        calendar_id = data.get('calendar_id')
        time_slots = data.get('time_slots')

        if not calendar_id or not time_slots:
            return JsonResponse({'error': 'Missing calendar_id or time_slots in the payload'}, status=400)

        calendar = get_object_or_404(Calendar, pk=calendar_id)

        if calendar.finalized:
            return JsonResponse({'error': 'Calendar is finalized, no modifications allowed'}, status=400)

        for slot in time_slots:
            if not all(k in slot for k in ['meeting_id', 'start_time', 'end_time', 'preference']):
                return JsonResponse({'error': 'Missing data in one of the time slots'}, status=400)

            meeting = get_object_or_404(Meeting, pk=slot['meeting_id'], calendar=calendar)

            Preference.objects.update_or_create(
                user=request.user,
                meeting=meeting,
                defaults={
                    'start_time': slot['start_time'],
                    'end_time': slot['end_time'],
                    'preference_level': slot['preference']
                }
            )

        return JsonResponse({'message': 'Preferences updated successfully'})

    except Calendar.DoesNotExist:
        return JsonResponse({'error': 'Calendar not found'}, status=404)
    except Meeting.DoesNotExist:
        return JsonResponse({'error': 'Meeting not found in this calendar'}, status=404)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key in payload: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def move_meeting_time(request):
    meeting_id = request.data.get('meeting_id')
    new_time_slot = request.data.get('new_time_slot')

    if not meeting_id or not new_time_slot:
        return Response({'error': 'Missing meeting_id or new_time_slot'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

    new_start_time = parse_datetime(new_time_slot['start_time'])
    new_end_time = parse_datetime(new_time_slot['end_time'])

    if not new_start_time or not new_end_time:
        return Response({'error': 'Invalid new_time_slot format'}, status=status.HTTP_400_BAD_REQUEST)

    conflicting_meetings = Meeting.objects.filter(
        calendar=meeting.calendar,
        start_time__lt=new_end_time,
        end_time__gt=new_start_time
    ).exclude(pk=meeting_id)

    if conflicting_meetings.exists():
        return Response({'error': 'Time slot is not available'}, status=status.HTTP_400_BAD_REQUEST)

    meeting.start_time = new_start_time
    meeting.end_time = new_end_time
    meeting.save()

    return Response({'message': 'Meeting time updated successfully'}, status=status.HTTP_200_OK)





@api_view(['POST'])

@permission_classes([IsAuthenticated])
def remind_users(request):
    meeting_id = request.data.get('meeting_id')
    contact_ids = request.data.get('contact_ids')

    if not meeting_id or not contact_ids:
        return Response({'error': 'Missing meeting_id or contact_ids'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

    for i in contact_ids:
        try:
            contact = Contact.objects.get(pk=i)  
            send_reminder(contact.email, meeting)
        except Contact.DoesNotExist:
            continue

    return Response({"message": "Reminders sent successfully"}, status=status.HTTP_200_OK)

def send_reminder(email, meeting):
    subject = f'Reminder for Meeting: {meeting.name}'
    message = f'Hi, this is a reminder about the meeting "{meeting.name}" scheduled on {meeting.date}. Provide your availability.'
    email_from = 'test@gmail.com' 
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_calendar_finalization(request, id):
    calendar = get_object_or_404(Calendar, pk=id)

    finalized_status = request.data.get('finalized', None)

    if finalized_status is None or not isinstance(finalized_status, bool):
        return Response({'error': 'Invalid finalized status provided.'}, status=status.HTTP_400_BAD_REQUEST)

    calendar.finalized = finalized_status
    calendar.save()

    status_message = 'finalized' if finalized_status else 'not finalized'
    return Response({'message': f'Calendar has been successfully {status_message}.'}, status=status.HTTP_200_OK)