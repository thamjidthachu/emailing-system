from django.urls import path, include
from django.conf import settings

app_name = "api_v1"

urlpatterns = [

    path('email/', include('apps.emails.urls', namespace='email')),

]
