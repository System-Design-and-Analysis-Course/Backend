from rest_framework import serializers

from user.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'username', 'phone_number')
        extra_kwargs = {'username': {'required': False}}

    def validate_phone_number(self, phone_number):
        if not phone_number.isdigit():
            raise serializers.ValidationError({"phone_number": "incorrect phone number format"})
        return phone_number


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Customer.objects.create_user(validated_data['username'], validated_data['username'],
                                            validated_data['password'])

        return user
