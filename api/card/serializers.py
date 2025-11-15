import json
from rest_framework import serializers
from .models import Card, Feedback
from api.file.models import FileCard
from api.file.serializers import FileCardSerializer

import re
class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:

        model = Feedback
        fields = '__all__'

        extra_kwargs = {
            'card': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }

        read_only_fields = [
            'card', 'created_at', 'updated_at'
        ]



class CardSerializer(serializers.ModelSerializer):

    feedback = FeedbackSerializer(required=False)

    class Meta:

        model = Card
        fields = '__all__'

        extra_kwargs = {
            'board': {'required': False},
            'feedback': {'required': False},
            'is_active': {'required': False},
            'approved_date': {'required': False},
            'deleted_at': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }

        read_only_fields = [

            'board', 'is_active', 'approved_date',
            'deleted_at', 'created_at', 'updated_at'

        ]

    def get_feedback(self, obj):

        feedback = obj.feedbacks.first()

        return FeedbackSerializer(feedback).data if feedback else None
    
    def get_all_files(self, obj):
        
        return FileCardSerializer(obj.files.all(), many=True).data

    def create(self, validated_data):

        feedback_data = validated_data.pop('feedback', None)

        card = Card.objects.create(**validated_data)

        if feedback_data:

            if isinstance(feedback_data, str):

                feedback_data = json.loads(feedback_data)

            Feedback.objects.create(card=card, **feedback_data)

        else:
            
            Feedback.objects.create(card=card)

        return card


    def update(self, instance, validated_data):

        feedback_data = validated_data.pop('feedback', None)
        
        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if feedback_data is not None:

            if isinstance(feedback_data, str):

                feedback_data = json.loads(feedback_data)

            feedback, _ = Feedback.objects.get_or_create(card=instance)

            for attr, value in feedback_data.items():

                setattr(feedback, attr, value)

            feedback.save()

        return instance
    
    @staticmethod
    def delete(instance):
        
        instance.delete()
        return instance


