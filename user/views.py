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
            #CLIENT_ID  = request.headers.get('client', None)
            token        = request.headers.get('token', None)
            data         = id_token.verify_oauth2_token(token, requests.Request())
            email        = data['email']
            user, flag   = User.objects.get_or_create(email=email)
            if flag:
                token        = jwt.encode({'id':user.id}, SECRET_KEY_JWT, ALGORITHM)
                access_token = token.decode('utf-8')
                context = {
                    'accessToken': access_token
                }
                return JsonResponse({'result':context}, status=200)
            return JsonResponse({'message':'Success'}, status=200)
        except ValueError:
            return JsonResponse({'message':'Invalid_token'}, status=400)


class RegisterView(View):

    def post(self, request):

        try:
            data = json.loads(request.body)
            if not validate_email(data['email']):
                return JsonResponse({'message':'Invalid_mail'}, status=400)
            if not validate_password(data['password']):
                return JsonResponse({'message':'Invalid_password'}, status=400)
            if User.objects.filter(email=data['email']):
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


class LoginView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            user =  User.objects.filter(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')):
                token        = jwt.encode({'id':user[0].id}, SECRET_KEY_JWT, ALGORITHM)
                access_token = token.decode('utf-8')
                context      = {
                    'accessToken': access_token,
                    'username': user[0].email.split('@')[0]
                }
                return JsonResponse({'result': context}, status=200)
            return JsonResponse({'message':'Invalid_user'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
        except IndexError:
            return JsonResponse({'message':'Invalid_user'}, status=400)


class BookmarkView(View):

    @login_decorator
    def post(self, request):
        try:
            if request.user:
                data = json.loads(request.body)
                if Bookmark.objects.filter(property_id=data['propertyId'], user_id=request.user.id).exists():
                    return JsonResponse({'message':'Already_exist'}, status=400)
                Bookmark.objects.create(property_id=data['propertyId'], user_id=request.user.id)
                return JsonResponse({'message':'Success'}, status=200)
            return JsonResponse({'message':'Invaild_user'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            if request.user:
                data = json.loads(request.body)
                if Bookmark.objects.filter(property_id=data['propertyId'], user_id=request.user.id).exists():
                    bookmark_query = Bookmark.objects.get(property_id=data['propertyId'], user_id=request.user.id)
                    bookmark_query.delete()
                    return JsonResponse({'message':'Success'}, status=200)
            return JsonResponse({'message':'Invaild_user'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
