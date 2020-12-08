import json
from datetime         import datetime

from django.http      import JsonResponse

from django.views     import View
from django.db.models import Q, Avg, Count

from .models          import Property, PropertyImage
from core.utils       import login_decorator, date_parser, check_availability, validate_check_in_out_date, validate_date_format, validate_review_set

class PropertyListView(View):

    @login_decorator
    def get(self, request):
        try:
            sort         = request.GET.get('sort', '0')
            limit        = int(request.GET.get('limit', 100000000000))
            offset       = int(request.GET.get('offset', 0))

            category     = request.GET.get('category', None)
            type         = request.GET.get('type', None)
            facility     = request.GET.getlist('facility', None)
            rule         = request.GET.get('rule', None)
            is_supered   = request.GET.get('is_super', None)
            max          = request.GET.get('max', '100000000')
            min          = request.GET.get('min', '0')

            check_in = request.GET.get('check_in', '5000-01-01')


            sort_set={
                '0': 'id',
                '1': '-review_count'
            }

            if not validate_date_format(check_in):
                return JsonResponse({'message':'Invalid_date_format'}, status=400)

            check_out = request.GET.get('check_out', '5000-01-10')
            if not validate_date_format(check_out):
                return JsonResponse({'message':'Invalid_date_format'}, status=400)

            number_of_guest = request.GET.get('guest', None)
            search          = request.GET.get('search', None)
            conditions      = {}
            available_rooms = []

            query  = Q()
            if search:
                query  &=\
                    Q(country__name__contains  = search) |\
                    Q(province__name__contains = search) |\
                    Q(city__name__contains     = search) |\
                    Q(district__name__contains = search) |\
                    Q(street__contains         = search)

            if category:
                conditions['category__id'] = category
            if type:
                conditions['type__id'] = type
            if facility:
                conditions['facility__id__in'] = facility
            if number_of_guest:
                conditions['capacity__lte'] = number_of_guest
            if check_in:
                check_in  = date_parser(check_in)
            if check_out:
                check_out = date_parser(check_out)

            if not validate_check_in_out_date(check_in, check_out):
                return JsonResponse({'message':'Invalid_date'}, status=400)

            if rule:
                conditions['rule__in'] = rule
            if is_supered:
                conditions['host__is_super'] = is_supered
            if min:
                conditions['price__gte'] = min
            if max:
                conditions['price__lte'] = max

            properties = Property.objects.\
                prefetch_related('propertyimage_set',
                                 'bookmark_set',
                                 'review_set',
                                 'type').\
                annotate(review_count=Count('review')).\
                filter(query, **conditions).order_by(sort_set[sort])

            available_rooms = [property for property in properties if check_availability(property, check_in, check_out)]

            context = [
                {
                    'cateoryName'     : property.category.name,
                    'porpertyType'    : property.type.name,
                    'propertyId'      : property.id,
                    'propertyName'    : property.title,
                    'price'           : property.price,
                    'propertyImages'  : [image.url for image in property.propertyimage_set.all()],
                    'hostName'        : property.host.name,
                    'isSuper'         : property.host.is_super,
                    'isBookmarked'    : property.bookmark_set.filter(user=request.user).exists(),
                    'longitude'       : property.longitude,
                    'latitude'        : property.latitude,
                    'capacity'        : property.capacity,
                    'facilities'      : [facility.name for facility in property.facility.all()[0:3]],
                    'size'            : [size.name for size in property.size.all()],
                    'numberOfReviews' : property.review_set.count(),
                    'rate'            : validate_review_set(property)
                }
                for property in  available_rooms[offset:offset+limit]
            ]

            return JsonResponse({'result':context}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)


class PropertyDetailView(View):

    @login_decorator
    def get(self, request, property_id):
        try:

            property = Property.objects.\
                select_related('host',
                               'refund').\
                prefetch_related('review_set',
                                 'review_set__user',
                                 'size',
                                 'rule',
                                 'safety',
                                 'facility').\
                get(id=property_id)

            conditions = {}
            conditions['price__lte'] = property.price + 50000
            conditions['price__gte'] = property.price - 50000

            properties = Property.objects.select_related('host').prefetch_related('propertyimage_set').filter(**conditions)[0:12]

            context = {
                'propertyId'     : property.id,
                'propertyName'   : property.title,
                'rate'           : {
                    'propertyRate'         : validate_review_set(property),
                    'propertyCleanliness'  : property.review_set.aggregate(Avg('cleanliness'))['cleanliness__avg'],
                    'propertyCommunication' : property.review_set.aggregate(Avg('communication'))['communication__avg'],
                    'propertyCheckIn'       : property.review_set.aggregate(Avg('check_in'))['check_in__avg'],
                    'propertyAccuracy'      : property.review_set.aggregate(Avg('accuracy'))['accuracy__avg'],
                    'propertyLocation'      : property.review_set.aggregate(Avg('location'))['location__avg'],
                    'propertyAffordability' : property.review_set.aggregate(Avg('affordability'))['affordability__avg']
                },

                'propertyImages' : [image.url for image in property.propertyimage_set.all()],
                'country'        : property.country.name,
                'province'       : property.province.name,
                'district'       : property.district.name,
                'price'          : property.price,
                'pricePerGuest'  : property.price_per_guest,
                'hostName'       : property.host.name,
                'isSupered'      : property.host.is_super,
                'isBookmarked'   : property.bookmark_set.filter(user=request.user).exists(),
                'capacity'       : property.capacity,
                'longitude'      : property.longitude,
                'latitude'       : property.latitude,
                'sizes'          : [
                    {
                        'sizeName'   : size.name,
                        'sizeContent': size.content
                    }
                    for size in property.size.all()
                ],
                'facilities': [facility.name for facility in property.facility.all()],
                'rules'     : [rule.name for rule in property.rule.all()],
                'safeties'  : [safety.name for safety in property.safety.all()],
                'refund'    : property.refund.content,
                'reviews'   : [
                    {
                        'user'           : review.user.email.split('@')[0],
                        'created_at'     : review.created_at,
                        'content'        : review.content,
                        'cleanliness'    : review.cleanliness,
                        'communications' : review.communication,
                        'checkIn'        : review.check_in,
                        'accuracy'       : review.accuracy,
                        'location'       : review.location,
                        'affordability'  : review.affordability
                    }
                    for review in property.review_set.all()
                ],
                'moreProperties':[
                    {
                        'propertyId'    : property.id,
                        'propertyName'  : property.title,
                        'propertyImage' : [image.url for image in property.propertyimage_set.all()],
                        'price'         : property.price,
                        'isSupered'       : property.host.is_super,
                        'isBookmarked'  : property.bookmark_set.filter(user=request.user).exists(),
                        'sizes': [
                            {
                                'sizeName'   : size.name,
                                'sizeContent': size.content
                            }
                            for size in property.size.all()
                        ]
                    }
                    for property in properties
                ]
            }
            return JsonResponse({'result':context}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
