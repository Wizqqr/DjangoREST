import random
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserConfirmSerializer
from .models import Profile
from django.core.mail import send_mail


def generate_confirmation_code():
    return ''.join(random.choices('0123456789', k=6))

def send_confirmation_email(user, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'DjangoRest5 <aziretkrutdzumabekov@gmail.com>'
    recipient_list = [user.email]
    html_message = f'''
       <html>
           <head>
               <style>
                   .container {{
                       max-width: 600px;
                       margin: 0 auto;
                       padding: 20px;
                       font-family: Arial, sans-serif;
                       border: 1px solid #e2e2e2;
                       border-radius: 10px;
                       background-color: #f9f9f9;
                   }}
                   .header {{
                       text-align: center;
                       padding-bottom: 20px;
                   }}
                   .code {{
                       font-size: 24px;
                       font-weight: bold;
                       text-align: center;
                       color: #4CAF50;
                   }}
                   .footer {{
                       margin-top: 20px;
                       text-align: center;
                       font-size: 12px;
                       color: #888;
                   }}
               </style>
           </head>
           <body>
               <div class="container">
                   <div class="header">
                       <h2>Подтверждение регистрации</h2>
                   </div>
                   <p>Здравствуйте, {user.username}!</p>
                   <p>Ваш код подтверждения:</p>
                   <div class="code">{confirmation_code}</div>
                   <p>Пожалуйста, введите этот код для завершения регистрации.</p>
                   <div class="footer">
                       <p>Спасибо за регистрацию!</p>
                   </div>
               </div>
           </body>
       </html>
       '''
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

@api_view(['POST'])
def registration_api_view(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')

        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

        confirmation_code = generate_confirmation_code()
        Profile.objects.create(user=user, confirmation_code=confirmation_code)

        send_confirmation_email(user, confirmation_code)

        return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def authorization_api_view(request):
    if request.method == 'POST':
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'The user is not authorized or confirmed'})

@api_view(['POST'])
def confirm_user_api_view(request):
    if request.method == 'POST':
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid username or confirmation code'})

        if profile.confirmation_code == confirmation_code:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK, data={'message': 'User confirmed successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code'})
