from rest_framework import serializers
from orders.models import Order
from django.contrib.auth.models import User


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ('url', 'id', 'user', 'status', 'begin_date', 'end_date', )
