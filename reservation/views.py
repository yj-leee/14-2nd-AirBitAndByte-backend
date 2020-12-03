import json

from django.http import JsonResponse
from django.views       import View

from reservation.models import Reservation
from core.utils         import dateParser

class ReservationCreateView(View):

    def post(self, request):
        try:
            data            = json.loads(request.body)
            check_in        = dateParser(data['checkIn'])
            check_out       = dateParser(data['checkOut'])
            Reservation.objects.create(
                user_id     = data['userId'],
                property_id = data['propertyId'],
                check_in    = check_in,
                check_out   = check_out,
                size_id     = data['sizeId'],
                status_id   = data['statusId']
            )
            return JsonResponse({'message': 'Success'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
