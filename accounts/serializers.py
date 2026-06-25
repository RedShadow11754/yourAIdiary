from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import UserPersonality


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True,min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')
    def create(self, validated_data):
        user = User.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password']
        )
        UserPersonality.objects.create(
            user=user
        )
        return user
