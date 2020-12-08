import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, Count

from .models import Property

class PropertiesView(View):
    def get(self, request):
        try:
            type_id     = request.GET.getlist('type')
            facility_id = request.GET.getlist('facility')
            min_price   = request.GET.get('min_price')
            max_price   = request.GET.get('max_price')
            ordering    = request.GET.get('ordering')
            search      = request.GET.get('search')
            properties  = Property.objects.select_related('country', 'province', 'city', 'district', 'host', 'type')\
                                         .prefetch_related('review_set')

            filters = {}

            if type_id:
                filters['type__id__in'] = type_id

                properties = properties.filter(**filters)

            if facility_id:
                filters['facility__id__in'] = facility_id

                properties = properties.filter(**filters)

            if min_price and max_price:
                filters['price__range'] = min_price, max_price

                properties = properties.filter(**filters)

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
                properties = properties.annotate(review_count = Count('review')).order_by(sort_type_set[ordering])

            q = Q()

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
            } for property in properties.filter(q)]

            return JsonResponse({'properties': properties, 'sortings':sortings}, status=200)

        except ValueError:
            return JsonResponse({'message': "VALUE_ERROR"}, status=400)
