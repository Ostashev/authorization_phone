from rest_framework import serializers

from users.models import UserProfile


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number']


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['invite_code']


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'phone_number',
            'verification_code',
            'verified',
            'invite_code',
            'activated_invite_code',
            'invited_users'
        ]

    def get_invited_users(self, obj):
        invited_users = UserProfile.objects.filter(
            activated_invite_code=obj.invite_code).exclude(
            phone_number=obj.phone_number
        )
        return UserInfoSerializer(invited_users, many=True).data


class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'verification_code'
        ]


class PhoneNumberInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'phone_number'
        ]


class VerificationSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField()
    verification_code = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'verification_code',
        ]
