import jwt
import re
import json

from datetime           import datetime

from django.http        import JsonResponse

from my_settings        import SECRET_KEY_JWT, ALGORITHM
from user.models        import User
from property.models    import Property
from reservation.models import Reservation

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            if not access_token:
                request.user = False
                return func(self, request, *args, **kwargs)
            payload      = jwt.decode(access_token, SECRET_KEY_JWT, algorithm=ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            pass

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper


def validate_email(email):
    return re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z]+\.[a-z.]+$', email)

def validate_password(password):
    return len(password) > 5

def validate_phone_number(phone_number):
    return re.match('^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$', phone_number)

#only works if date format(2020-02-06)
def dateParser(date):
    date_list = date.split('-')
    year      = int(date_list[0])
    month     = int(date_list[1])
    day       = int(date_list[2])
    date_time = datetime(year, month, day)
    return date_time

def checkAvailability(property, check_in, check_out):
    bookings      = Reservation.objects.filter(property_id=property.id)
    check_in      = datetime.date(check_in)
    check_out     = datetime.date(check_out)
    avalilability = []
    for booking in bookings:
        #   check_in: 2020-01-09,   check_out: 2020-01-11
        # b_check_in: 2020-01-05, b_check_out: 2020-01-08
        if booking.check_in > check_out or booking.check_out < check_in:
            avalilability.append(True)
        else:
            avalilability.append(False)
    return all(avalilability)
