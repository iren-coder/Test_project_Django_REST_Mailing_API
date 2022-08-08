from django.urls import path
from rest_framework import routers
from mailing import views
from mailing.views import MailingLoginView, MailingSignupView, MailingLogoutView, CreateUserProfile
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


from mailing.views import (
    ClientViewSet,
    MailingViewSet,
    MailingListAPIView,
)


urlpatterns = [

    path(r'maillists/', MailingListAPIView.as_view(), name='maillists'),
]
router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'mailings', MailingViewSet, basename='mailing')

urlpatterns += router.urls