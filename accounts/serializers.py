from rest_framework import serializers

from accounts.models import User, Client
from profiles.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ClientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ('user', 'manager', 'passport_number')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts:client-detail',
        lookup_field='pk'
    )
    user = UserSerializer('user', many=False, read_only=True)

    class Meta:
        model = Client
        fields = ('url', 'pk', 'user', 'is_active')


class InactiveProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts:profile-detail',
        lookup_field='pk'
    )
    client = serializers.ReadOnlyField(source='client.user.email')

    class Meta:
        model = Profile
        fields = ('url', 'pk', 'client', 'is_active')
