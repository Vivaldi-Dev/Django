from rest_framework import serializers
from .models import Post

class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        
        def create(self, validated_data):
    
            return Post.objects.create(**validated_data)

