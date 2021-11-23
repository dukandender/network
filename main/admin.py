from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Post,Comment
from .forms import UserCreationForm

# Register your models here.

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Profile',
            {
                'fields': (
                    'full_name',
                    'bio',
                    'birth_date',
                    'avatar',
                    'following'
                ),
            },
        ),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)