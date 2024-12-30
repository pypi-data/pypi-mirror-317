from adrf.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from ovinc_client.account.models import User

USER_MODEL: User = get_user_model()


class UserInfoSerializer(ModelSerializer):
    """
    User Info
    """

    class Meta:
        model = USER_MODEL
        fields = ["username", "nick_name", "user_type", "last_login"]
