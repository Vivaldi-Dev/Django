import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import Userserializers
from .models import User

class Register(APIView):
    def post(self, request):
        serializers = Userserializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=400)
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        
        refresh = RefreshToken.for_user(user)
        
        response = Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name 
            }
        })
        
        response.set_cookie(key='refresh_jwt', value=str(refresh), httponly=True)
        
        return response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("Request headers:", request.headers)
        print("User:", request.user)
        user = request.user
        return Response({
            'message': 'You are authorized to view this data.',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        })
