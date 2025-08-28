from django.contrib import admin

from .models import Board

@admin.register(Board)
class BoardModelAdmin(admin.ModelAdmin):

    list_display = [

        'customer', 'created_at', 'updated_at'

    ]

    list_filter = [

        'customer'

    ]