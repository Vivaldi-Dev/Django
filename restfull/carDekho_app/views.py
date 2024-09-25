from django.shortcuts import render
from .models import carlist
from .models import Showroomlist, carlist
from .serializers import CarSerializers
from .serializers import Showroomlistserializers
from .serializers import SerializerReview
from .models import Review
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import generics

# from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SerializerObjectCar

#authentication
from rest_framework.authentication import BaseAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated




# 1. Views Baseadas em Classe (CBV) -> É mais organizado e facilita a adição de métodos adicionais e a herança de comportamento entre views.
class Showroom_View(APIView):
    
    # authentication_classes = [BaseAuthentication]
    permission_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        showroom = Showroomlist.objects.all()
        serializers = Showroomlistserializers(showroom, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = Showroomlistserializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.data)
# show object(get com dicionario)
class showobject(APIView):
  def get(self,request):
      showcar = carlist.objects.all()
      serializres = SerializerObjectCar(showcar,many=True)
      response_data={
          'status':status.HTTP_200_OK,
          'data':serializres.data
      }
      return Response(response_data)


# show users
class showUser(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class Showroom_detail(APIView):
    def get(self, request, pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            response_data = {
                "erros": "Showroom not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return {response_data}
        Serializer = Showroomlistserializers(showroom)
        return Response(Serializer.data)

    def put(self, request, pk):
        showroom = Showroomlist.objects.get(pk=pk)
        serializer = Showroomlistserializers(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Showroom = Showroomlist.objects.get(pk=pk)
        Showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views Baseadas em Função (FBV) -> Mais simples e direta, especialmente para views simples.
@api_view(["GET", "POST"])
def car_list(request):
    if request.method == "GET":
        car = carlist.objects.all()
        serializers = CarSerializers(car, many=True)
        data = serializers.data
        response_data = {"status": status.HTTP_200_OK, "data": data}
        return Response(response_data)

    if request.method == "POST":
        serializers = CarSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            data = serializers.data
            response_data = {"status": status.HTTP_201_CREATED, "data": data}
            return Response(response_data)
        else:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializers.errors,
            }
            return Response(response_data)


@api_view(["GET", "PUT", "DELETE"])
def car_detail_view(request, pk):
    if request.method == "GET":
        # car = carlist.objects.get(pk=pk)
        car = get_object_or_404(carlist, pk=pk)
        serializer = CarSerializers(car)
        return Response(serializer.data)

    if request.method == "PUT":
        car = get_object_or_404(carlist, pk=pk)
        serializer = CarSerializers(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {"status": status.HTTP_200_OK, "data": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        car = get_object_or_404(carlist, pk=pk)
        car.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# generics view
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = SerializerReview

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin,  generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = SerializerReview
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class Reviewdetail(generics.RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class=SerializerReview

# def car_list(request):
#     cars = carlist.objects.all()
#     data={
#         'cars':list(cars.values())

#     }
#     #  return JsonResponse(data)
#     dat_json = json.dumps(data)
#     return HttpResponse(dat_json, content_type='application/json')

# def car_detail_view(request,pk):
#     car = carlist.objects.get(pk=pk)
#     data = {
#         'name':car.name,
#         'description':car.description,
#         'active':car.active
#     }

#     return JsonResponse(data)
