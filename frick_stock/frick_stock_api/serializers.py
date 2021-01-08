from rest_framework import serializers
from .models import *


class FollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__" # ("user", "name",)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ('balance', )


class CurrentClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = "__all__"