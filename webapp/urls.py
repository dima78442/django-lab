from django.urls import path
from webapp import views
from webapp.models import ConnectedUsers
from .views import send_email_task, do_long_work_task, list_finished_tasks

urlpatterns = [
    path('run_task/send_email/', send_email_task),
    path('run_task/do_long_work/', do_long_work_task),
    path('list_finished_task/', list_finished_tasks),
    path('online/', views.users_online),
    path('', views.index, name='index'),
    path('<str:person_id>/', views.person_info, name='person_id'),
]

ConnectedUsers.objects.all().delete()
