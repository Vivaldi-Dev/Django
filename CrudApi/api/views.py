from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializers

@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializers = UserSerializers(users,many=True)
        return Response(serializers.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_nick(request, nick):
    try:
       users = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET':
        serializers = UserSerializers(users)   
        return Response(serializers.data) 
   
   