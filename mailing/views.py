from django.shortcuts import redirect, render
from rest_framework import generics, mixins, viewsets
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse_lazy
from allauth.account.views import SignupView, LoginView, LogoutView
from django.views.generic import FormView
from mailing.forms import ProfileCreationForm

from .models import Client, Mailing, UserProfile
from .serializers import (
    ClientSerializer,
    MailingSerializer,
    MailingListSerializer
)

# Create your views here.

# Redefine allauth.account.views
class MailingSignupView(SignupView):
    success_url = reverse_lazy('links')
    template_name = 'allauth/account/signup.html'


class MailingLoginView(LoginView):
    success_url = reverse_lazy('links')
    template_name = 'allauth/account/login.html'


class MailingLogoutView(LogoutView):
    success_url = reverse_lazy('login')
    template_name = 'allauth/account/logout.html'

def index(request):
    template = loader.get_template('index.html')
    context = {}
    if request.user.is_authenticated:
        try:
            context['username'] = request.user.username
            context['user'] = UserProfile.objects.get(user=request.user).age
            context['github_url'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']
        except:
            pass

    return HttpResponse(template.render(context, request))

def links(request):
    template = loader.get_template('links.html')
    data = {
        "title": "Все роуты проекта",
    }
    return HttpResponse(template.render(data, request))


# Creating a user profile
class CreateUserProfile(FormView):
    form_class = ProfileCreationForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('mailing:links')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('mailing:MailingLoginView'))
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(CreateUserProfile, self).form_valid(form)


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MailingViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


class MailingListAPIView(generics.ListAPIView):
    queryset = Mailing.objects.raw('''
       SELECT  sender_maillist.id id,
                start_at,
                finish_at,
                operator_code_id,
                tag_id,
                status_pending,
                status_failed,
                status_success
        FROM    sender_maillist
        LEFT JOIN (
            SELECT maillist_id, COUNT(*) AS "status_pending"
            FROM sender_message
            GROUP BY maillist_id, status
			HAVING status LIKE "Pending"
        ) t1
        ON      sender_maillist.id=t1.maillist_id
        LEFT JOIN (
            SELECT maillist_id, COUNT(*) AS "status_success"
            FROM sender_message
            GROUP BY maillist_id, status
			HAVING status LIKE "Success"
        ) t2
        ON      sender_maillist.id=t2.maillist_id
        LEFT JOIN (
            SELECT maillist_id, COUNT(*) AS "status_failed"
            FROM sender_message
            GROUP BY maillist_id, status
			HAVING status LIKE "Failed"
        ) t3
        ON      sender_maillist.id=t3.maillist_id
    ''')
    serializer_class = MailingListSerializer


