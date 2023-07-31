from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(UserModelViewSet, self).get_queryset()
        return queryset.filter(id=self.request.user.id)
