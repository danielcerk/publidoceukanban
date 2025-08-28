from django.contrib import admin

from .models import Card, Feedback

@admin.register(Card)
class CardModelAdmin(admin.ModelAdmin):

    list_display = [

        'title', 'board', 'status',
        'is_active', 'start_date', 'due_date',
        'created_at', 'updated_at'

    ]

    list_filter = [

        'title', 'board', 'status', 'is_active'

    ]

@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):

    list_display = [

        'card', 'text'

    ]

    list_filter = [

        'card'

    ]