import json
from datetime import datetime

from django.http      import JsonResponse

from django.views     import View
from django.db.models import Q

from .models          import Property, PropertyImage
from core.utils       import dateParser, checkAvailability, login_decorator

class PropertySearchView(View):
    def get(self, request):
        try:
            check_in        = request.GET.get('check_in', '5000-01-01')
            check_out       = request.GET.get('check_out', '5000-01-01')
            guest           = request.GET.get('guest', None)
            search          = request.GET.get('search', None)
            conditions      = {}
            available_rooms = []

            if search:
                query = Q()
                query  &=\
                    Q(country__name__contains  = search) |\
                    Q(province__name__contains = search) |\
                    Q(city__name__contains     = search) |\
                    Q(district__name__contains = search) |\
                    Q(street__contains         = search)

#                properties = Property.objects.prefetch_related('propertyimage_set', 'bookmark_set', 'review_set').\
#                    filter(Q(country__name__contains  =search) |\
#                           Q(province__name__contains =search) |\
#                           Q(city__name__contains     =search) |\
#                           Q(district__name__contains =search) |\
#                           Q(street__contains         =search) |\
#                           Q(title__contains          =search))
            if guest:
                conditions['capacity__lte'] = guest
#                properties = properties.filter(capacity__lte=guest)
            if check_in:
                check_in  = dateParser(check_in)
            if check_out:
                check_out = dateParser(check_out)

            properties = Property.objects.\
                prefetch_related('propertyimage_set', 'bookmark_set', 'review_set').\
                filter(**conditions)

            for property in properties:
                if checkAvailability(property, check_in, check_out):
                    available_rooms.append(property)

            context =[
                {
                    'propertyId'    : property.id,
                    'propertyName'  : property.title,
                    'propertyImage' : [image.url for image in property.propertyimage_set.all()],
                    'capacity'      : property.capacity,
                    'price'         : property.price,
                    'reviewRate'    : [
                        ((review.cleanliness +\
                         review.communication +\
                         review.check_in +\
                         review.accuracy +\
                         review.location +\
                         review.affordability)/6) for review in property.review_set.all()],
                    'longitude'     : property.longitude,
                    'latitude'      : property.latitude
                }
                for property in available_rooms
            ]
            available_rooms=[]
            return JsonResponse({'result':context}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)


class PropertyListView(View):

    def get(self, request):
        try:
            category   = request.GET.get('category', None)
            type       = request.GET.get('type', None)
            rule       = request.GET.get('rule', None)
            is_supered = request.GET.get('is_super', None)
            min        = request.GET.get('min', '0')
            max        = request.GET.get('max', '100000000')


            conditions = {}

            if category:
                conditions['category__id'] = category
            if type:
                conditions['type__id']     = type

            rule_set = [
                {
                    '7': '흡연금지',
                    '8': '반려동물동반불가',
                    '9': '파티나이벤트금지'
                }
            ]

            if rule:
                conditions['rule']         = rule

            # input: Ture/False
            if is_supered:
                conditions['host__is_super'] = is_supered
            if min:
                conditions['price__gte']   = min
            if max:
                conditions['price__lte']   = max


            sort_set={
                '0': 'reviews'
            }

            properties = Property.objects.select_related('host').prefetch_related('review_set', 'facility', 'size','rule', 'review_set').filter(**conditions)

            context = [
                {
                    'propertyId'      : property.id,
                    'propertyName'    : property.title,
                    'hostName'        : property.host.name,
                    'isSuper'         : property.host.is_super,
                    'longitude'       : property.longitude,
                    'latitude'        : property.latitude,
                    'capacity'        : property.capacity,
                    'numberOfReviews' : property.review_set.count(),
                    'facilities'      : [ facility.name for facility in property.facility.all()[0 : 3]],
                    'size'            : [size.name for size in property.size.all()],
                    'rate'            : [
                        ((review.cleanliness +\
                          review.communication +\
                          review.check_in +\
                          review.accuracy +\
                          review.location +\
                          review.affordability)/6) for review in property.review_set.all()
                    ],


                }
                for property in properties
            ]

            return JsonResponse({'result':context}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)


class PropertyDetailView(View):

    def get(self, request, property_id):
        try:
            property = Property.objects.\
                select_related('host').\
                prefetch_related('review_set', 'review_set__user','size', 'rule', 'facility').\
                get(id=property_id)
            context = {
                'propertyId': property.id,
                'propertyName': property.title,
                'hostName': property.host.name,
                'is_supered': property.host.is_super,
                'capacity': property.capacity,
                'longitude': property.longitude,
                'latitude': property.latitude,
                'sizes': [
                    {
                        'sizeNmae':size.name,
                        'sizeContent': size.content
                    }
                    for size in property.size.all()
                ],
                'facilities': [facility.name for facility in property.facility.all()],
                'rules':[rule.name for rule in property.rule.all()],
                'revies': [
                    {
                        'user': review.user.email,
                        'content': review.content,
                        'cleanliness': review.cleanliness,
                        'communications': review.communication,
                        'checkIn': review.check_in,
                        'accuracy': review.accuracy,
                        'location': review.location,
                        'affordability': review.affordability
                    }
                    for review in property.review_set.all()
                ]
            }
            return JsonResponse({'result':context}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)




