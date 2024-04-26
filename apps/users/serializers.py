from rest_framework import serializers
from apps.users.models import User, Address


class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        user = User.objects.create(**validated_data)

        for address_data in addresses_data:
            Address.objects.create(user=user, **address_data)
        return user

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])  # Extract addresses data

        # Update user fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        # Update addresses
        for address_data in addresses_data:
            address_id = address_data.get('id', None)
            if address_id:
                # If address ID is provided, update existing address
                address = Address.objects.get(id=address_id)
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                # If no address ID is provided, create a new address
                Address.objects.create(user=instance, **address_data)

        return instance
