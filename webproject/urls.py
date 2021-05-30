from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from webapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'person', views.PersonViewSet, 'person')
router.register(r'phone', views.PhoneViewSet, 'phone')


urlpatterns = [
    path('', include(router.urls)),
    path('account/register', views.UserCreate.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi',
         get_schema_view(
            title="webapp",
            description="Simple blog, "
                        "the API can store sme info about person and its phone numbers",
            version="1.0.0"
         ),
         name='openapi-schema'),
    path('redoc/',
         TemplateView.as_view(
                    template_name='redoc.html',
                    extra_context={'schema_url': 'openapi-schema'}
         ),
         name='redoc'),

    path('swagger-ui/',
         TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
         ),
         name='swagger-ui'),
]
