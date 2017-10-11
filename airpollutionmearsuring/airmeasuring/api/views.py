from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import permissions
from django.contrib.auth.models import User
from dashboard.models import Area, Data, RawData
from manage_devices.models import Node


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerialization
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminPermission,)


class AreaModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AreaSerialization
    queryset = Area.objects.all()
    permission_classes = (permissions.IsAdminPermission,)


class DataModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DataSerialization
    queryset = Data.objects.all()
    permission_classes = (permissions.IsAdminPermission,)


class RawDataModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RawDataSerialization
    queryset = RawData.objects.all()
    permission_classes = (permissions.IsAdminPermission,)


class NodeModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NodeSerialization
    queryset = Node.objects.all()
    permission_classes = (permissions.IsAdminPermission,)
