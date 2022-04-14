from rest_framework import generics, status, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import User
from .permissions import IsPMO, IsOwnerOrPMO
from django.contrib.auth import get_user_model


# Register API
class RegisterAPI(generics.GenericAPIView):
    name = 'register'
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "details": "User resgistered succesfully!",
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]                
            },
            status=status.HTTP_201_CREATED
        )


# Login API
class LoginAPI(generics.GenericAPIView):
    name = 'login'
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user = UserSerializer(user_data, context=self.get_serializer_context()).data
        
        # delete any token belonging to this user before issuing another
        AuthToken.objects.filter(user=user_data).delete()

        auth_token = AuthToken.objects.create(user=user_data)[1]

        return  Response(
                {
                    'user': user,
                    'auth_token': auth_token
                }, 
                status=status.HTTP_200_OK
            )         


#   Get single user instance
class UserDetailsAPI(generics.RetrieveAPIView): 
    name = 'user-details'
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrPMO)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


#   Get user list
class UserListAPI(generics.ListAPIView): 
    name = 'user-list'
    permission_classes = (permissions.IsAuthenticated, IsPMO)
    users = get_user_model().objects.all()
    # exclude admin users from total list
    queryset = users.exclude(is_superuser=True) 
    serializer_class = UserSerializer


#   Activate user account
class ActivateUserAPI(generics.GenericAPIView):
    name = 'activate-user'
    permission_classes = (permissions.IsAuthenticated, IsPMO)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
            return Response(
                    {'detail': 'User activated successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )
        except User.DoesNotExist:
            return Response(
                    {'detail': 'User does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )


#   Deactivate user account
class DeactivateUserAPI(generics.GenericAPIView):
    name = 'deactivate-user'
    permission_classes = (permissions.IsAuthenticated, IsPMO)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save()
            return Response(
                    {'detail': 'User deactivated successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )
        except User.DoesNotExist:
            return Response(
                    {'detail': 'User does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )


    