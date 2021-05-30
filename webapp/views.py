from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url
from .models import Person, Phone, ConnectedUsers
from .serializers import PersonSerializer, PhoneSerializers
from django.http import HttpResponse
from django.shortcuts import render


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PersonSerializer


class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PhoneSerializers


def index(request):
    persons = [person for person in Person.objects.all()]
    return render(request, 'index.html', {
        'persons': persons
    })


def person_info(request, person_id):
    # Send article by id to user
    person = Person.objects.get(id=person_id)
    phones = [phone for phone in Phone.objects.filter(person_id=person_id)]
    if person:
        return render(request, 'person_info.html', {
            'person_id': person_id,
            'phones': phones,
            'person': person
        })
    else:
        return HttpResponse('Wrong person id')


def users_online(request):
    if request.user.is_authenticated:
        connected_users = [user for user in ConnectedUsers.objects.all()]
        return render(request, 'online.html', {
            'connected_users': connected_users
        })
