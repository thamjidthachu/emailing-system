from django.urls import path

from .views import MailSendView

app_name = 'emails'

urlpatterns = [
	path('send/', MailSendView.as_view(), name="send"),
]
