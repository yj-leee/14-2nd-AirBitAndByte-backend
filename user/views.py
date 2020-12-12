import json
import requests

from django.views import View
from django.http  import JsonResponse


from    property.models   import (Property,PropertyImage,Host,Type,Attribute,PropertyAttributes,
                                  Refund,Size,PropertySizes,Facility,PropertyFacilities,Review,
                                  Safety,PropertySafeties,Rule,PropertyRules,Comment,Country,
                                  Province,City,District)
from    .models           import  User, Bookmark


class BookMarkView(View):
    def get(self, request):
        user_id   = request.user

        queryset  = Bookmark.objects.filter(user_id=user_id)

        result = [{
            'title'            : bookmark.property.title,
            'Price'            : bookmark.property.price,
            'capacity'         : bookmark.property.capacity,
            'latitude'         : bookmark.property.latitude,
            'longitude'        : bookmark.property.longitude,
            'image'            : [{'url' : image.url} for image in property.propertyimage_set.all()],
            'SuperHost'        : bookmark.property.host.is_super,
            'type'             : bookmark.property.type.name,
            'facility'         : [facility.name for facility in bookmark.property.facility.all()],
            'category'         : bookmark.property.category.name,
            'num_reviews'      : bookmark.property.num_reviews,
            'rule'             : [rule.name for rule in bookmark.property.rule.all()]
    } for bookmark in queryset]

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id      = data['user_id']
            property_id  = data['property_id']

            if Bookmark.objects.filter(user_id=user_id, property_id=property_id).exists():
                return JsonResponse({'MESSAGE' : 'ERROR'}, status=400)

            Bookmark.objects.create(user_id=user_id, property_id=property_id)
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

    def delete(self, request, bookmark_id):
        try:
            if not Bookmark.objects.filter(user_id=user_id, property_id=property_id).exists():
                return JsonResponse({'MESSAGE' : 'ERROR'}, status=400)
            bookmark = Bookmark.objects.filter(user_id=user_id, property_id=property_id)
            bookmark.delete()

            result = {
                'MESSAGE' : 'SUCCESS'
            }

            return JsonResponse(result, status=204)

        except KeyError:
            return JsonResponse(result, status=400)
