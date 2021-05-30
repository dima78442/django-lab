from django.urls import path
from webapp import views
from webapp.models import ConnectedUsers


urlpatterns = [
    path('online/', views.users_online),
    path('', views.index, name='index'),
    path('<str:person_id>/', views.person_info, name='person_id'),
]

ConnectedUsers.objects.all().delete()