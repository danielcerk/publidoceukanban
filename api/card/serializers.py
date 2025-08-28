from rest_framework import serializers
from .models import Card, Feedback
from api.supabase_utils import upload_to_supabase


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
    image_upload = serializers.ImageField(write_only=True, required=False)
    feedback = FeedbackSerializer(read_only=True)

    class Meta:
        model = Card
        fields = '__all__'
        extra_kwargs = {
            'board': {'required': False},
            'is_activee': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }
        read_only_fields = ['board', 'is_active', 'created_at', 'updated_at']

    def get_feedback(self, obj):

        feedback = obj.feedbacks.first()

        if feedback:

            return FeedbackSerializer(feedback).data
        
        return None

    def create(self, validated_data):
        feedback_data = validated_data.pop('feedback', None)
        image_file = validated_data.pop('image_upload', None)

        if image_file:
            validated_data['image'] = upload_to_supabase(image_file)

        card = super().create(validated_data)

        Feedback.objects.create(card=card)

        return card

    def update(self, instance, validated_data):
        feedback_data = validated_data.pop('feedback', None)
        image_file = validated_data.pop('image_upload', None)

        if image_file:
            validated_data['image'] = upload_to_supabase(image_file)

        card = super().update(instance, validated_data)

        if feedback_data is not None:

            feedback, created = Feedback.objects.get_or_create(card=card)

            for attr, value in feedback_data.items():

                setattr(feedback, attr, value)

            feedback.save()

        return card