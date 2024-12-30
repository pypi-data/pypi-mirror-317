from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from django.utils.translation import gettext_lazy

from ovinc_client.account.models import User
from ovinc_client.core.utils import strtobool


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "nick_name", "user_type", "date_joined", "last_login"]
    list_filter = ["user_type"]
    search_fields = ["username", "nick_name"]


class ExpiredFilter(SimpleListFilter):
    title = gettext_lazy("Is Expired")
    parameter_name = "is_expired"

    def lookups(self, request, model_admin):
        return (
            (True, gettext_lazy("Yes")),
            (False, gettext_lazy("No")),
        )

    def queryset(self, request, queryset):
        if self.value():
            is_expired = strtobool(self.value())
            if is_expired:
                return queryset.filter(expired_at__lt=timezone.now())
            return queryset.filter(expired_at__gte=timezone.now())
        return queryset
