"""P2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('calendars/', views.calendar),
    path('calendars/<int:id>/initiate_meeting/', views.meeting),
    path('meetings/<int:id>/set_preference/', views.preference),
    path('meetings/<int:id>/proposals/', views.schedule_proposals),
    path('meetings/<int:id>/finalized/', views.schedule_get_finalize),
    path('meetings/<int:meeting_id>/finalized/<int:schedule_id>/', views.schedule_make_finalize),
    path('meetings/<int:meeting_id>/preference/<int:preference_id>/', views.preference_update),
   path('calendars/<int:id>/modify/', views.modify_non_busy_times, name='modify_non_busy_times'),
    path('meetings/move/', views.move_meeting_time),
    path('schedule/meetings/remind/', views.remind_users),
    path('calendars/<int:id>/finalization/', views.update_calendar_finalization, name='update_calendar_finalization'),
]
