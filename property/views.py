import  json
import  requests

from    django.views     import  View
from    django.http      import  JsonResponse

from    django.db.models import Q, Count

from    .models          import  (Property,PropertyImage,Host,Type,Attribute,PropertyAttributes,
                                  Refund,Size,PropertySizes,Facility,PropertyFacilities,Review,
                                  Safety,PropertySafeties,Rule,PropertyRules,Comment,Country,
                                  Province,City,District)


class MainListView(View):
    def get(self, request):
        host      = request.GET.get("host")
        type      = request.GET.get("type")
        review    = request.GET.get("review")
        facility  = request.GET.get("facility")
        category  = request.GET.get("category")
        rule      = request.GET.get("rule")

        q = Q()

        if host:
            q &= Q(host__is_super=host)

        if type:
            q &= Q(type__name=type)

        if facility:
            q &= Q(facility__name=facility)

        if category:
            q &= Q(category__name=category)

        if rule:
            q &= Q(rule__name=rule)

        queryset = Property.objects.filter(q)

        if review:
            queryset = queryset.annotate(num_reviews=Count('review')).order_by('-num_reviews')

        result = [{
                'title'            : property.title,
                'Price'            : property.price,
                'capacity'         : property.capacity,
                'latitude'         : property.latitude,
                'longitude'        : property.longitude,
                'image'            : [{'url' : image.url} for image in property.propertyimage_set.all()],
                'SuperHost'        : property.host.is_super,
                'type'             : property.type.name,
                'facility'         : [facility.name for facility in property.facility.all()],
                'category'         : property.category.name,
                'num_reviews'      : property.num_reviews,
                'rule'             : [rule.name for rule in property.rule.all()]
        } for property in queryset]

        return JsonResponse( {'data' : result} , status=200)





