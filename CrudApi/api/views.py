from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializers


# GET all
@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializers = UserSerializers(users,many=True)
        return Response(serializers.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
# GET By name
@api_view(['GET'])
def get_nick(request, nick):
    try:
       users = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET':
        serializers = UserSerializers(users)   
        return Response(serializers.data) 
    
# GET com parametros   
@api_view (['GET'])
def get_all(request): 
    
    if request.method == 'GET':
        
        try:
            if request.GET['user']:
                user_nickname = request.GET['user']
                try:
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response (status=status.HTTP_404_NOT_FOUND)
                serializers = UserSerializers(user)
                return Response(serializers.data)
                
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)            

@api_view(['POST'])
def post_data(request):
    if request.method == 'POST':
        new_user = request.data 
        serializers = UserSerializers(data=new_user)
        
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST )
    
@api_view (['GET'])
def put_data(request):
    if request.method == 'PUT':
        nickname = request.data['user_nickname']   
        
        update_user = User.objects.get(pk=nickname)
        
        print(request.data)
        
        serializers = UserSerializers(update_user,data=request.data)
        
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST) 