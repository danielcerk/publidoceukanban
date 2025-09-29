from rest_framework import serializers

from .models import Checklist

class ChecklistSerializer(serializers.ModelSerializer):

    class Meta:

        model = Checklist
        fields = '__all__'

        extra_kwargs = {

            'id': {'required': False},
            'card': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False}

        }

        read_only_fields = [

            'id', 'card', 'created_at', 'updated_at'

        ]