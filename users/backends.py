from django.contrib.auth.backends import BaseBackend

from .models import UserProfile


class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, verification_code=None):
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            if user.verification_code == verification_code:
                return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None
