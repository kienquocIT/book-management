from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from .authentication import CustomTokenObtainPairSerializer
from ..models import User, UploadedFile
from .serializers import UserCreateSerializer, UserRegisterSerializer, UserLoginSerializer, UserListSerializer, \
    UserDetailSerializer, UserUpdateSerializer, UploadedFileSerializer, UploadAvatarSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserListSerializer(user, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    user = User.objects.filter(pk=pk).first()
    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Username or password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Upload Image
class FileUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser,)  # For web forms
    serializer_class = UploadedFileSerializer
    queryset = UploadedFile.objects.all()

    def perform_create(self, serializer):
        serializer.save(file=self.request.data.get('file'))

class AvatarUploadView(generics.UpdateAPIView):
    permission_classes([IsAuthenticated])
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = UploadAvatarSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(file=self.request.data.get('file'))