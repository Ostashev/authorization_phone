import random
import time

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserProfile


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            user, created = UserProfile.objects.get_or_create(
                phone_number=phone_number)
            if created:
                verification_code = ''.join(random.choices('0123456789', k=4))
                user.verification_code = verification_code
                user.save()
                time.sleep(random.uniform(1, 2))
                message = f"Код верификации: {verification_code}"
            else:
                message = "Этот номер телефона уже зарегистрирован."
            return render(request, 'signup.html', {'message': message})
    return render(request, 'signup.html')


def login_view(request):
    response_message = None

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        verification_code = request.POST.get('verification_code')
        if phone_number and verification_code:
            try:
                user = UserProfile.objects.get(phone_number=phone_number)
                if user.verification_code == verification_code:
                    user.verified = True
                    user.save()
                    user = authenticate(
                        request,
                        phone_number=phone_number,
                        verification_code=verification_code
                    )
                    if user is not None:
                        login(request, user)
                        response_message = 'Проверка прошла успешно!'
                else:
                    response_message = 'Неверный код!'
            except UserProfile.DoesNotExist:
                response_message = 'Пользователь не найден!'
    return render(
        request,
        'login.html',
        {'response_message': response_message}
    )


@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(
        phone_number=request.user.phone_number)
    response_message = None

    if request.method == 'POST':
        invite_code = request.POST.get('invite_code')
        if invite_code:
            try:
                invited_user = UserProfile.objects.get(invite_code=invite_code)
                if user_profile != invited_user and \
                        not user_profile.activated_invite_code:
                    user_profile.activated_invite_code = invite_code
                    user_profile.save()
                    response_message = 'Код успешно активирован!'
                else:
                    response_message = 'Неверный код!'
            except UserProfile.DoesNotExist:
                response_message = 'Код не найден!'
    invite_codes = UserProfile.objects.filter(
        activated_invite_code=user_profile.invite_code)
    return render(
        request,
        'user_profile.html',
        {
            'user_profile': user_profile,
            'invite_codes': invite_codes,
            'response_message': response_message
        }
    )
