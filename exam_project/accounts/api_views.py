from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .serializers import AppUserSerializer, AppUserUpdateSerializer

User = get_user_model()


class MeRetrieveUpdateApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return AppUserUpdateSerializer
        return AppUserSerializer


class UsersListApiView(generics.ListAPIView):
    serializer_class = AppUserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class SignUpApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name', '')

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=400)
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"detail": e.messages}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered."}, status=400)

        user = User.objects.create_user(email=email, password=password, full_name=full_name)
        return Response({"id": user.id, "email": user.email}, status=201)
