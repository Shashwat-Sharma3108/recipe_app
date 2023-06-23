
from .serializers import (
    UserSerializers, 
    UserTokenSerializer
    )

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializers

class CreateUserTokenView(ObtainAuthToken):
    serializer_class = UserTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES #Optional ----> For Interactive UI

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializers
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
