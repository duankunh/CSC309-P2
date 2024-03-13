from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Contact
from .serializers import ContactSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def contact_list_create(request):
    if request.method == 'GET':
        contacts = Contact.objects.filter(owner=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                owner=request.user)  # Set the owner to the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.


@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def update_delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, owner=request.user)
    if contact.owner != request.user:
        return Response({"detail": "Not authorized to modify this contact"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        print("here")
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
