from rest_framework import serializers
# from itdtool.models import UserAction
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

