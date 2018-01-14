from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import permissions
from django.contrib.auth.models import User
from dashboard.models import Area, Data, RawData, AQI
from manage_devices.models import Node


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerialization
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminPermission,)


class AreaModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AreaSerialization
    queryset = Area.objects.all()
    permission_classes = ()


class DataModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DataSerialization
    queryset = Data.objects.all()
    permission_classes = ()


class RawDataModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RawDataSerialization
    queryset = RawData.objects.all()
    permission_classes = ()


class NodeModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NodeSerialization
    queryset = Node.objects.all()
    permission_classes = ()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        else:
            return self.queryset.filter(user=user)


class AQIModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AQISerialization
    queryset = AQI.objects.all()
    permission_classes = ()
