import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, Count, Avg

from .models import Property

class PropertiesView(View):
    def get(self, request):
        try:
            type_id     = request.GET.getlist('type')
            facility_id = request.GET.getlist('facility')
            min_price   = request.GET.get('min_price')
            max_price   = request.GET.get('max_price')
            ordering    = request.GET.get('ordering')
            offset      = int(request.GET.get('offset', 0))
            limit       = int(request.GET.get('limit', offset + 10))
            search      = request.GET.get('search')
            properties  = Property.objects.select_related('country', 'province', 'city', 'district', 'host', 'type')\
                                          .prefetch_related('review_set')

            filter_set = {}

            if type_id:
                filter_set['type__id__in'] = type_id
            if facility_id:
                filter_set['facility__id__in'] = facility_id
            if min_price and max_price:
                filter_set['price__range'] = min_price, max_price

            properties = properties.filter(**filter_set)

            sort_type_set = {
                '0': '-review_count'
            }

            sortings = [
                {
                    'id': 0,
                    'name': '리뷰 많은순',
                }
            ]

            if ordering in sort_type_set:
                properties = properties.annotate(review_count = Count('review'))\
                                       .order_by(sort_type_set[ordering])

            q = Q()

            # q.add(Q(country__name='한국'), q.AND)

            if search:
                q &= Q(country__name=search) | Q(province__name=search) | Q(city__name=search) | Q(district__name=search)

            properties = [{
                'title'       : property.title,
                'country'     : property.country.name,
                'province'    : property.province.name,
                'city'        : property.city.name,
                'district'    : property.district.name,
                'street'      : property.street,
                'is_super'    : property.host.is_super,
                'type'        : property.type.name,
                'capacity'    : property.capacity,
                # 'price'       : property.price,
                'size'        : property.size.count(),
                'review_count': property.review_set.count(),
                'latitude'    : property.latitude,
                'longitude'   : property.longitude,
                'facilities'  : [
                    facility.name for facility in property.facility.all()
                ]
            } for property in properties.filter(q)[offset:limit + offset]]

            return JsonResponse({'properties': properties, 'sortings': sortings}, status=200)

        except ValueError:
            return JsonResponse({'message': "VALUE_ERROR"}, status=400)

class PropertyDetailView(View):
    def get(self, request, property_id):
        try:
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', offset + 5))
            properties = Property.objects.all()

            property = properties.get(id=property_id)

            detail = {
                'propertyId': property.id,
                'propertyName': property.title,
                'country': property.country.name,
                'province': property.province.name,
                'district': property.district.name,
                'price': property.price,
                'pricePerGuest': property.price_per_guest,
                'hostName': property.host.name,
                'isSupered': property.host.is_super,
                # 'isBookmarked': property.bookmark_set.filter(user=request.user).exists(),
                'capacity': property.capacity,
                'longitude': property.longitude,
                'latitude': property.latitude,
                'sizes': [
                    {
                        'sizeNmae': size.name,
                        'sizeContent': size.content
                    }
                    for size in property.size.all()
                ],
                'facilities': [facility.name for facility in property.facility.all()],
                'rules': [rule.name for rule in property.rule.all()],
                'safeties': [safety.name for safety in property.safety.all()],
                'rufund': property.refund.content,
                'review': {
                    'review_count': property.review_set.count(),
                    'reviews': [
                    {
                        'user': review.user.email.split('@')[0],
                        'created_at': review.created_at,
                        'content': review.content,
                    } for review in property.review_set.all()[offset:limit]
                    ],
                'review_avg': {
                    'cleanliness_avg': property.review_set.aggregate(Avg('cleanliness'))["cleanliness__avg"],
                    'communication_avg': property.review_set.aggregate(Avg('communication'))['communication__avg'],
                    'checkIn_avg': property.review_set.aggregate(Avg('check_in'))['check_in__avg'],
                    'accuracy_avg': property.review_set.aggregate(Avg('accuracy'))['accuracy__avg'],
                    'location_avg': property.review_set.aggregate(Avg('location'))['location__avg'],
                    'affordability_avg': property.review_set.aggregate(Avg('affordability'))['affordability__avg']
                    },
                'review_total_avg': round((property.review_set.aggregate(Avg('cleanliness'))["cleanliness__avg"] +
                                     property.review_set.aggregate(Avg('communication'))['communication__avg'] +
                                     property.review_set.aggregate(Avg('check_in'))['check_in__avg'] +
                                     property.review_set.aggregate(Avg('accuracy'))['accuracy__avg'] +
                                     property.review_set.aggregate(Avg('location'))['location__avg'] +
                                     property.review_set.aggregate(Avg('affordability'))['affordability__avg']
                                     ) / 6, 2)
                },
                'moreProperties': [
                    {
                        'propertyId': property.id,
                        'propertyName': property.title,
                        'propertyImage': [image.url for image in property.propertyimage_set.all()],
                        'price': property.price,
                        'isSuper': property.host.is_super,
                        # 'isBookmarked': property.bookmark_set.filter(user=request.user).exists(),
                        'sizes': [
                            {
                                'sizeName': size.name,
                                'sizeContent': size.content
                            }
                            for size in property.size.all()
                        ]
                    }
                    for property in properties
                ]
            }

            return JsonResponse({'properties': detail}, status=200)

        except ValueError:
            return JsonResponse({'message': "VALUE_ERROR"}, status=400)
