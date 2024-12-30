from django.contrib.auth import get_user_model
from rest_framework.response import Response

from ovinc_client.account.models import User
from ovinc_client.account.serializers import UserInfoSerializer
from ovinc_client.core.viewsets import ListMixin, MainViewSet

USER_MODEL: User = get_user_model()


class UserInfoViewSet(ListMixin, MainViewSet):
    """
    User Info
    """

    queryset = USER_MODEL.objects.all()

    async def list(self, request, *args, **kwargs):
        """
        User Info
        """

        return Response(await UserInfoSerializer(request.user).adata)
