from django.contrib import admin


from django.contrib.auth.admin import UserAdmin 
from .models import Product, User, Category, Size, Gender
from django.utils.translation import gettext_lazy as _


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )



# Register your models here.
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Gender)
