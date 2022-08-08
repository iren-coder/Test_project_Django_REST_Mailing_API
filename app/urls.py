"""app URL Configuration

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
from django.views.generic import TemplateView
from django.urls import include, path
from rest_framework.schemas import get_schema_view
from mailing import views
from mailing.views import MailingLoginView, MailingSignupView, MailingLogoutView, CreateUserProfile
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

schema_url_patterns = [
    path('api/v1/', include('mailing.urls')),
]


urlpatterns = [
    path('', views.links, name='links'),
    path('admin/', admin.site.urls),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url': 'openapi-schema'},
    ), name="docs"),

    path('openapi/', get_schema_view(
        title="Mailing service",
        description="API",
        version="1.0.0",
        patterns=schema_url_patterns,
    ), name='openapi-schema'),

    path('api-auth/', include('rest_framework.urls')),

    path('api/v1/', include('mailing.urls')),

    path('accounts/', include('allauth.urls')),
]