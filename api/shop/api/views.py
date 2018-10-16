import datetime

import math

import io
import os
from wsgiref.util import FileWrapper

import pytz
import xlsxwriter
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from urllib.parse import urlparse, parse_qs

from shop.api.models import Job, StatusType

from shop.api.serializers import KeypoUserSerializer


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(hours=3):
            raise AuthenticationFailed('Token has expired')

        return token.user, token


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        print(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'username': request.user.username,
            'email': request.user.email,
            'groups': [g.name for g in request.user.groups.all()],
            'is_active': request.user.is_active,
            'is_superuser': request.user.is_superuser,
            'user_permissions': [{
                'name': p.name,
                'codename': p.codename,
            } for p in request.user.user_permissions.all()],
            'last_login': request.user.last_login,
            'date_joined': request.user.date_joined,
        }
        return Response(content)


class Logout(APIView):
    # authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class InScheduledJob(APIView):
    # authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        jobs = Job.objects.filter(status=StatusType.INSCHEDULED.value).all()

        serializer = KeypoUserSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, format=None):
        request.POST._mutable = True

        print(request.data)
        id = request.data['id']

        request.data['status'] = StatusType.DONE.value

        job = Job.objects.filter(id=id).first()

        job.total_count = request.data['total_count']
        job.skip_count = request.data['skip_count']
        job.filename = request.data['filename']
        job.status = StatusType.DONE.value
        job.save()

        return Response(
            'ok',
            status=status.HTTP_200_OK
        )

        # serializer = KeypoUserSerializer(
        #     job,
        #     data=job
        # )
        #
        # if serializer.is_valid():
        #     serializer.save()
        #     print(f"{request.data} save ok")
        #     return Response(
        #         'ok',
        #         status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(
        #         serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST
        #     )


class AllJob(APIView):
    # authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        jobs = Job.objects.order_by("created_at").all()

        serializer = KeypoUserSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, format=None):
        request.POST._mutable = True

        query_url = request.data['query_url']

        if not query_url or len(query_url) <= 0:
            return HttpResponseRedirect(redirect_to=request.META['HTTP_REFERER'])

        url_obj = urlparse(query_url)
        query_obj = parse_qs(url_obj.query)
        title = query_obj['as_q'][0]

        skip_url = request.data.get('skip_url', "")

        job = Job()
        job.query_url = query_url
        job.skip_url = skip_url
        job.title = title
        job.save()

        return HttpResponseRedirect(redirect_to=request.META['HTTP_REFERER'])


class Excel(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        id = self.request.query_params.get('id', None)

        if not id:
            return Response(
                    'no id',
                    status=status.HTTP_400_BAD_REQUEST
                )

        request.data['status'] = StatusType.DONE.value

        job = Job.objects.filter(id=id).first()

        filename = job.filename

        with open(f"/data/{filename}", "r") as excel:
            data = excel.read()

        response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s_Report.xlsx' % id
        return response