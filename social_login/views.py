# backend/social-login/views.py

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json

#from django.contrib.auth.decorators import login_required
#from django.utils.decorators import method_decorator

#@method_decorator(login_required, name='dispatch')
"""
class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        output = []
        return HttpResponse(json.dumps(output))

    def post(self, request, *args, **kwargs):
        print(request.data)
        print(request.headers)
        output = []
        return HttpResponse(json.dumps(output))
"""

class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/login"
    client_class = OAuth2Client
