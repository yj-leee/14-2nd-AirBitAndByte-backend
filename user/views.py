import jwt
import bcrypt
import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from user.models import User
from my_settings import SECRET_KEY_JWT, ALGORITHM
from user.utils import validate_email, validate_password, validate_phone_number

class Register(View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            if not validate_email(data['email']):
                return JsonResponse({'message':'Invalid_mail'}, status=400)
            if not validate_password(data['password']):
                return JsonResponse({'message':'Invalid_password'}, status=400)
            if not validate_phone_number(data['phone_number']):
                return JsonResponse({'message':'Invalid_phone_number'}, status=400)

            if User.objects.filter(email=data['email']):
                return JsonResponse({'message':'User_already_exist'}, status=400)

            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cryped_password = hashed_password.decode('utf-8')

            User.objects.create(
                email        = data['email'],
                phone_number = data['phone_number'],
                image_url    = data['image_url'],
                first_name   = data['first_name'],
                last_name    = data['last_name'],
                password     = cryped_password
            )
            return JsonResponse({'message':'Success'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)


class Login(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.filter(Q(email=data['key']) | Q(phone_number=data['key']))
            if bcrypt.checkpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')):
                token        = jwt.encode({'id':user[0].id}, SECRET_KEY_JWT, ALGORITHM)
                access_token = token.decode('utf-8')

                context = {
                    'access_token': access_token,
                    'username': user[0].email
                }

                return JsonResponse({'result': context}, status=200)
            return JsonResponse({'message':'Success'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
        except IndexError:
            return JsonResponse({'message':'Invalid_user'}, status=400)

