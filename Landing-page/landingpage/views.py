from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import BlogSerializers
from rest_framework.views import APIView
from .models import Post
from rest_framework import mixins
from rest_framework import generics

class BlogView(GenericAPIView):
    queryset = Post.objects.all()  
    serializer_class = BlogSerializers

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    