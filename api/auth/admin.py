from django.contrib import admin
from .models import UserProfile, Profile

@admin.register(UserProfile)
class UserProfileModelAdmin(admin.ModelAdmin):

    list_display = (

        'name', 'first_name', 'last_name', 'email',
        'is_superuser', 'is_staff', 'is_active',
        'created_at', 'updated_at'
        
    )

    list_filter = (

        'is_superuser', 'is_staff', 'is_active'

    )

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):

    list_display = (

        'user', 'slug', 'whatsapp',

    )