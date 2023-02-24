from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from panel.models import Library, CustomDate
from user.models import Customer


class CustomDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomDate
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=Customer.objects.all())
    date_info = CustomDateSerializer(required=False)

    class Meta:
        model = Library
        fields = ('id', 'name', 'content_type', 'user', 'date_info')
        extra_kwargs = {'date_info': {'required': False}}

    def create(self, validated_data):
        date_info = CustomDate(created_at=now(), last_modified_at=now())
        date_info.save()
        validated_data['date_info'] = date_info
        return super(LibrarySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        date_info = instance.date_info
        date_info.last_modified_at = now()
        date_info.save()
        validated_data['date_info'] = date_info
        return super(LibrarySerializer, self).update(instance, validated_data)
