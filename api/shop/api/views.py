import datetime

import math

import io
import os
from wsgiref.util import FileWrapper

import pytz
import xlsxwriter
from django.contrib.auth.models import User
from django.http import HttpResponse
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