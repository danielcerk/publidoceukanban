import json
from rest_framework import serializers
from .models import Card, Feedback
from api.supabase_utils import upload_to_supabase, delete_from_supabase

from api.card.utils import file_compress

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

    file_upload = serializers.FileField(write_only=True, required=False)
    feedback = FeedbackSerializer(required=False)

    class Meta:
        
        model = Card
        fields = '__all__'
        extra_kwargs = {
            'board': {'required': False},
            'feedback': {'required': False},
            'image': {'required': False},
            'is_active': {'required': False},
            'approved_date': {'required': False},
            'deleted_at': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }
        read_only_fields = ['board', 'is_active', 'approved_date',
            'deleted_at', 'created_at', 'updated_at']

    def get_feedback(self, obj):

        feedback = obj.feedbacks.first()

        if feedback:

            return FeedbackSerializer(feedback).data
        
        return None

    def create(self, validated_data):

        feedback_data = validated_data.pop('feedback', None)
        uploaded_file = validated_data.pop('file_upload', None)

        if uploaded_file:

            #compress_file_uploaded = file_compress(uploaded_file)

            validated_data['image'] = upload_to_supabase(uploaded_file)

        card = super().create(validated_data)

        if isinstance(feedback_data, str):

            feedback_data = json.loads(feedback_data)

        if feedback_data is None:

            feedback_data = {}

        Feedback.objects.create(card=card)

        return card

    def update(self, instance, validated_data):

        feedback_data = validated_data.pop('feedback', None)
        uploaded_file = validated_data.pop('file_upload', None)

        if uploaded_file:

            if instance.image:

                delete_from_supabase(instance.image)

            validated_data['image'] = upload_to_supabase(uploaded_file)

        card = super().update(instance, validated_data)

        if feedback_data is not None:

            if isinstance(feedback_data, str):

                feedback_data = json.loads(feedback_data)

            feedback, _ = Feedback.objects.get_or_create(card=card)

            for attr, value in feedback_data.items():

                setattr(feedback, attr, value)
                
            feedback.save()

        return card

    
    def delete(self, instance):

        if instance.image:

            delete_from_supabase(instance.image)

        instance.delete()
