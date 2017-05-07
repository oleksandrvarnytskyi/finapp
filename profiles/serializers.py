from rest_framework import serializers

from profiles.models import Profile


class ProfileRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('client', 'pin_code')

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        profile = Profile.objects.create(client=client_data, **validated_data)
        return profile


class ProfileDetailViewSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.user.email')
    balance = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ('client', 'balance', 'pin_code', 'is_active')


class ProfileLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('client', 'pin_code')
