from django.urls import path
from .views import contact_list_create, update_delete_contact
from . import views

urlpatterns = [
    path('list/', contact_list_create, name='contact-list-create'),
    path('<int:contact_id>/', views.update_delete_contact, name='update-delete-contact')
]
