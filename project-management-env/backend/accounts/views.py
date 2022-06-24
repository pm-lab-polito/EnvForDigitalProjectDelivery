from rest_framework import generics, status, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import User
from custom_permissions.permissions import (IsProjectManagementOffice, 
        IsOwnerOrProjectManagementOffice)
from django.contrib.auth import get_user_model


# Register API
class RegisterAPI(generics.GenericAPIView):
    name = 'register'
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "detail": "User resgistered succesfully!",
                "user": UserSerializer(user, context=self.get_serializer_context()).data                
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
    permission_classes = (IsOwnerOrProjectManagementOffice,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


#   Get user list
class UserListAPI(generics.ListAPIView): 
    name = 'user-list'
    permission_classes = [IsProjectManagementOffice,]
    users = get_user_model().objects.all()
    # exclude admin users from total list
    queryset = users.exclude(is_superuser=True)
    queryset = queryset.exclude(email='AnonymousUser')
    serializer_class = UserSerializer


#   Activate user account
class ActivateUserAPI(generics.GenericAPIView):
    name = 'activate-user'
    permission_classes = [IsProjectManagementOffice,]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
            return Response(
                    {'detail': 'User activated successfully'},
                    status=status.HTTP_200_OK
                )

        except User.DoesNotExist:
            return Response(
                    {'detail': 'User does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )


#   Deactivate user account
class DeactivateUserAPI(generics.GenericAPIView):
    name = 'deactivate-user'
    permission_classes = [IsProjectManagementOffice,]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save()
            return Response(
                    {'detail': 'User deactivated successfully'},
                    status=status.HTTP_200_OK
                )
        except User.DoesNotExist:
            return Response(
                    {'detail': 'User does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )



#   Update user role as ProjectManagementOffice
class UpdateUserRoleAPI(generics.UpdateAPIView):
    name = 'update-user-role'
    serializer_class = UserSerializer
    permission_classes = [IsProjectManagementOffice,]
    queryset = User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

