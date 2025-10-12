from rest_framework import serializers
from .models import FileCard
from api.supabase_utils import upload_to_supabase, delete_from_supabase


class FileCardSerializer(serializers.ModelSerializer):

    file_upload = serializers.FileField(write_only=True, required=False)
    clear_file = serializers.BooleanField(write_only=True, required=False)
    delete = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = FileCard
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {'card': {'required': False}}

    def create(self, validated_data):
        validated_data.pop('clear_file', None)
        validated_data.pop('delete', None)
        file = validated_data.pop('file_upload', None)

        if file:
            try:
                validated_data['file'] = upload_to_supabase(
                    file,
                    original_name=file.name,
                    content_type=file.content_type
                )
            except ValueError as e:
                raise serializers.ValidationError({"file_upload": str(e)})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        file = validated_data.pop('file_upload', None)
        clear_file = validated_data.pop('clear_file', False)
        validated_data.pop('delete', None)

        if file:
            if instance.file:
                delete_from_supabase(instance.file)
            try:
                validated_data['file'] = upload_to_supabase(
                    file,
                    original_name=file.name,
                    content_type=file.content_type
                )
            except ValueError as e:
                raise serializers.ValidationError({"file_upload": str(e)})

        elif clear_file:
            if instance.file:
                delete_from_supabase(instance.file)
            validated_data['file'] = None

        return super().update(instance, validated_data)

    def delete(self, instance):
        if instance.file:
            delete_from_supabase(instance.file)
        instance.delete()
