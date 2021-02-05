import json

from django.http        import JsonResponse
from django.views       import View

from reservation.models import Reservation
from core.utils         import login_decorator, date_parser, check_availability
from property.models    import Property


class ReservationView(View):

    @login_decorator(required=True)
    def get(self, request):
        try:
            if not request.user:
                return JsonResponse({'message':'Invalid_user'}, status=400)

            status = request.GET.get('status', None)

            conditions = {}

            if status:
                conditions['status_id'] = status
            conditions['user_id']   = request.user.id

            bookings = Reservation.objects.select_related('user', 'property', 'size', 'status').filter(**conditions)
            context  = [
                {
                    'user'         : booking.user.email,
                    'property_id'  : booking.property.id,
                    'propertyName' : booking.property.title,
                    'checkIn'      : booking.check_in,
                    'checkout'     : booking.check_out,
                    'size'         : booking.size.name,
                    'sizeContent'  : booking.size.content,
                    'status'       : booking.status.name
                }
                for booking in bookings
            ]
            return JsonResponse({'result':context}, status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)

    @login_decorator(required=True)
    def post(self, request):
        try:
            data            = json.loads(request.body)
            check_in        = date_parser(data['checkIn'])
            check_out       = date_parser(data['checkOut'])

            if check_in == check_out:
                return JsonResponse({'message':'Not_Available'}, status=400)
            property = Property.objects.get(id=data['propertyId'])

            if not check_availability(property, check_in, check_out):
                return JsonResponse({'message':'Not_Available'}, status=400)

            Reservation.objects.create(
                user        = request.user,
                property_id = data['propertyId'],
                check_in    = check_in,
                check_out   = check_out,
                size_id     = data['sizeId'],
                status_id   = data['statusId']
            )
            return JsonResponse({'message': 'Success'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)


class PaymentView(View):

    @login_decorator(required=True)
    def patch(self, request, reservation_id):
        try:
            reservation           = Reservation.objects.get(id=reservation_id)
            reservation.status_id = 2
            reservation.save()
            return JsonResponse({'message':'Success'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
