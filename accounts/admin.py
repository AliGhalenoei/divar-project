from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User , OTP , UserProfile
from .forms import UserChangeForm , UserCreationForm



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['phone' , 'is_admin']
    list_filter = ['is_admin']
    search_fields = ['phone']
    filter_horizontal = ()
    ordering = ['phone']

    fieldsets = (
        ('User Information',{'fields':('phone','password','username')}),
        ('Permissions',{'fields':('is_active','is_admin','is_superuser')}),
    )

    add_fieldsets = (
        ('Create Account',{'fields':('phone','username','password','password2')}),
    )


admin.site.register(User,UserAdmin)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['phone' , 'code']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','id']

