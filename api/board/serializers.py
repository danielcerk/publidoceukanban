from rest_framework import serializers

from .models import Board

class BoardSerializer(serializers.ModelSerializer):

    class Meta:

        model = Board
        fields = '__all__'

        extra_kwargs = {

            'customer': {'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},

        }

        read_only_fields = [

            'customer', 'created_at', 'updated_at'

        ]