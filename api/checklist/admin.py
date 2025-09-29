from django.contrib import admin
from .models import Checklist

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'card',
        'title',
        'is_check',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'is_check',
        'created_at',
        'updated_at',
        'card',
    )

    search_fields = (
        'title',
        'card__customer__name',
    )

    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
