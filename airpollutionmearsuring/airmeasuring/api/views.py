from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import permissions
from django.contrib.auth.models import User


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerialization
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminPermission,)
