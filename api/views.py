import random
import time

from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import UserProfile

from .serializers import (InviteCodeSerializer, PhoneNumberInputSerializer,
                          PhoneNumberSerializer, UserProfileSerializer,
                          VerificationSerializer)


class CreateUserViewSet(viewsets.ViewSet):
    serializer_class = PhoneNumberInputSerializer

    def create_phone_number(self, request):
        serializer = PhoneNumberInputSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user, created = UserProfile.objects.get_or_create(
                phone_number=phone_number)
            if created:
                verification_code = ''.join(random.choices('0123456789', k=4))
                user.verification_code = verification_code
                user.save()
                time.sleep(random.uniform(1, 2))
                user_serializer = PhoneNumberSerializer(user)
                return Response(
                    user_serializer.data, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Данный номер уже зарегистрирован!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = self.create_phone_number(request)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(
                {'error': 'Данный номер уже зарегистрирован!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return response


class UserProfileViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return InviteCodeSerializer
        return UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(
            phone_number=self.request.user.phone_number)

    def create(self, request, *args, **kwargs):
        invite_code = request.data.get('invite_code')
        if invite_code:
            try:
                invited_user = UserProfile.objects.get(invite_code=invite_code)
                user_profile = self.get_queryset().first()
                if user_profile != invited_user and \
                        not user_profile.activated_invite_code:
                    user_profile.activated_invite_code = invite_code
                    user_profile.save()
                    return Response(
                        {'message': 'Код успешно активирован!'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': 'Неверный код!'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except UserProfile.DoesNotExist:
                return Response(
                    {'error': 'Код не найден!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'error': 'Invalid data'},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        verification_code = serializer.validated_data['verification_code']
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            if user.verification_code == verification_code:
                user.verified = True
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'message': 'Проверка прошла успешно!',
                        'token': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Неверный код!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден!'},
                status=status.HTTP_400_BAD_REQUEST
            )
