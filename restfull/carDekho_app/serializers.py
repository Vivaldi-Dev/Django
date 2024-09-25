from rest_framework import serializers
from .models import carlist
from .models import Showroomlist
from .models import Review
from django.contrib.auth.models import User


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = carlist
        fields = "__all__"

        def create(self, validated_data):

            return carlist.objects.create(**validated_data)


class Showroomlistserializers(serializers.ModelSerializer):
    class Meta:
        model = Showroomlist
        fields = "__all__"

        def create(self, validated_data):

            return carlist.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class SerializerObjectShowroom(serializers.ModelSerializer):
    class Meta:
        model = Showroomlist
        fields = ["id", "name"]

class SerializerObjectCar(serializers.ModelSerializer):
    showroom = SerializerObjectShowroom(read_only=True)
    model = carlist
    class Meta:
            model = carlist
            fields = ['id', 'name', 'description', 'active', 'chassinumber', 'price', 'showroom']

class SerializerReview(serializers.ModelSerializer):
   
    class Meta:
         model = Review 
         fields = "__all__"
         def create(self, validated_data):
    
            return carlist.objects.create(**validated_data)
            