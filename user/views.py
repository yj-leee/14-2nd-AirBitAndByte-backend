import jwt
import bcrypt
import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from user.models           import User, Bookmark
from my_settings           import SECRET_KEY_JWT, ALGORITHM
from core.utils            import validate_email, validate_password, validate_phone_number, login_decorator
from google.oauth2         import id_token
from google.auth.transport import requests


class SocialLoginView(View):

    def post(self, request):
        try:
            token        = request.headers.get('token', None)
            data         = id_token.verify_oauth2_token(token, requests.Request())
            email        = data['email']
            user, flag   = User.objects.get_or_create(email=email)
            if not flag:
                token        = jwt.encode({'id':user.id}, SECRET_KEY_JWT, ALGORITHM)
                access_token = token.decode('utf-8')
                return JsonResponse({'accessToken':access_token}, status=200)
            return JsonResponse({'message':'Success'}, status=200)
        except ValueError:
            return JsonResponse({'message':'Invalid_token'}, status=400)


class SignUpView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            if not validate_email(data['email']):
                return JsonResponse({'message':'Invalid_mail'}, status=400)
            if not validate_password(data['password']):
                return JsonResponse({'message':'Invalid_password'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'User_already_exist'}, status=400)

            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cryped_password = hashed_password.decode('utf-8')
            birth           = data['birthdayYear'] + '-' +  data['birthdayMonth'] + '-' + data['birthdayDate']

            User.objects.create(
                email        = data['email'],
                birthday     = birth,
                given_name   = data['givenName'],
                family_name  = data['familyName'],
                password     = cryped_password
            )
            return JsonResponse({'result':'Success'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)

class LogInView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            user =  User.objects.get(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token        = jwt.encode({'id':user.id}, SECRET_KEY_JWT, ALGORITHM)
                access_token = token.decode('utf-8')
                return JsonResponse({'accessToken': access_token}, status=200)
            return JsonResponse({'message':'Invalid_user'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'Does_not_exist'}, status=400)

class BookmarkView(View):

    @login_decorator(required=True)
    def post(self, request):
        try:
            data = json.loads(request.body)
            bookmark, flag = Bookmark.objects.get_or_create(property_id=data['propertyId'], user_id=request.user.id)
            if flag:
                return JsonResponse({'message':'Success'}, status=200)
            return JsonResponse({'message':'Invaild_command'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)

    @login_decorator(required=True)
    def delete(self, request):
        try:
            data = json.loads(request.body)
            if Bookmark.objects.filter(property_id=data['propertyId'], user_id=request.user.id).exists():
                bookmark_query = Bookmark.objects.get(property_id=data['propertyId'], user_id=request.user.id)
                bookmark_query.delete()
                return JsonResponse({'message':'Success'}, status=200)
            return JsonResponse({'message':'bookmark_does_not_exist'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
