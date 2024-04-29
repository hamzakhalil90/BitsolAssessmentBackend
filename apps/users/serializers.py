from rest_framework import serializers
from apps.users.models import User, Address


class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        data = super(UserDetailSerializer, self).to_representation(instance)
        data["addresses"] = AddressSerializer(
            instance.addresses.all(), many=True).data if instance.addresses.exists() else []
        return data

    def create(self, validated_data):
        addresses_data = self.context.get('address', [])
        user = User.objects.create(**validated_data)
        address_ids = []
        for address_data in addresses_data:
            address = Address.objects.create(user=user, **address_data)
            address_ids.append(address.id)
        user.addresses.set(address_ids)
        return user

    def update(self, instance, validated_data):
        addresses_data = self.context.get('address', [])  # Extract addresses data

        # Update user fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        # Update addresses
        address_ids = []
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
                address = Address.objects.create(user=instance, **address_data)
                address_ids.append(address.id)
        instance.addresses.add(*address_ids)
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
