from rest_framework import serializers

from .models import User, UserTask

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'