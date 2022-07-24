from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer, DetailUserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        user_serializer = DetailUserSerializer(request.user, context=dict(request=request))
        return Response(user_serializer.data)


