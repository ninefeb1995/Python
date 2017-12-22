from rest_framework import serializers
from django.contrib.auth.models import User
from dashboard.models import Area, Data, RawData, AQI
from manage_devices.models import Node


class UserSerialization(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_fullname(self, obj):
        return obj.first_name + ' ' + obj.last_name

    def create(self, validated_data):
        user = super(UserSerialization, self).create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if validated_data.get('password') != 'passwordisnotchange':
            instance.set_password(validated_data.get('password'))
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance


class AreaSerialization(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


class DataSerialization(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = '__all__'


class RawDataSerialization(serializers.ModelSerializer):

    class Meta:
        model = RawData
        fields = '__all__'


class NodeSerialization(serializers.ModelSerializer):
    area_name = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = '__all__'

    def get_area_name(self, obj):
        return obj.area.name


class AQISerialization(serializers.ModelSerializer):

    class Meta:
        model = AQI
        fields = '__all__'


