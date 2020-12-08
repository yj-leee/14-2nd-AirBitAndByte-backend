import json

from property.models import *
from django.test     import TestCase, Client
from unittest.mock   import patch, MagicMock

class PropertiesTest(TestCase):
    maxDiff = None

    def setUp(self):
        Category.objects.create(
            name='통나무집'
        )

        Type.objects.create(
            name='집 전체'
        )

        Host.objects.create(
            name='이성보',
            is_super=1
        )

        Attribute.objects.create(
            title='집 전체',
            content='펜션 전체를 단독으로 사용하시게 됩니다'
        )

        Refund.objects.create(
            content='체크인 3일 전까지 수수료 없이 취소 가능'
        )

        Size.objects.create(
            name='1번 침실',
            content='퀸사이즈 침대 1개'
        )

        Facility.objects.create(
            name='무선 인터넷'
        )

        # Review.objects.create(
        #     user=1,
        #     property=1,
        #     content='정말 짱입니다',
        #     cleanliness=4.00,
        #     communication =4.00,
        #     check_in =4.00,
        #     accuracy =4.00,
        #     location =4.00,
        #     affordability =4.00
        # )

        Safety.objects.create(
            name='코로나 조심'
        )

        Rule.objects.create(
            name='체크인 시간: 아무때나'
        )

        # Comment.objects.create(
        #     review=1,
        #     host=1,
        #     content='감사합니다'
        # )

        Country.objects.create(
            name='한국',
            latitude=33.455762,
            longitude=126.550932
        )

        Province.objects.create(
            name='제주도',
            latitude=33.455762,
            longitude=126.550932,
            country_id=1
        )

        City.objects.create(
            name='제주시',
            latitude=33.455762,
            longitude=126.550932,
            province_id=1
        )

        District.objects.create(
            name='애월읍',
            latitude=33.455769,
            longitude=126.550939,
            city_id=1
        )

        Property.objects.create(
            title='zzang',
            content='일단 오세요 짱입니다',
            capacity=2,
            price=90000.00,
            price_per_guest=26000.000,
            longitude=126.550931,
            latitude=33.455761,
            type_id=1,
            category_id=1,
            host_id=1,
            refund_id=1,
            country_id=1,
            province_id=1,
            city_id=1,
            district_id=1,
            street='아라1동 312-5'
        )

        PropertyImage.objects.create(
            property_id=1,
            url='https://www.facebook.com/'
        )

        PropertyAttributes.objects.create(
            property_id=1,
            attribute_id=1
        )

        PropertySizes.objects.create(
            property_id=1,
            size_id=1
        )

        PropertyFacilities.objects.create(
            property_id=1,
            facility_id=1
        )

        PropertyRules.objects.create(
            property_id=1,
            rule_id=1
        )

        PropertySafeties.objects.create(
            property_id=1,
            safety_id=1
        )

    def tearDown(self):
        Property.objects.all().delete()

    def test_properties_get_success(self):

        client = Client()
        response = client.get('/property?search=한국')

        matching_response = [{
                'title'       : property.title,
                'country'     : property.country.name,
                'province'    : property.province.name,
                'city'        : property.city.name,
                'district'    : property.district.name,
                'street'      : property.street,
                'is_super'    : property.host.is_super,
                'type'        : property.type.name,
                'capacity'    : property.capacity,
                'size'        : property.size.count(),
                'review_count': property.review_set.count(),
                'latitude'    : str(property.latitude),
                'longitude'   : str(property.longitude),
                'facilities'  : [
                    facility.name for facility in property.facility.all()
                ]
            } for property in Property.objects.filter(country__name = '한국')]

        sortings = [
            {
                'id': 0,
                'name': '리뷰 많은순',
            }
        ]

        self.assertEqual(response.json(), {'properties': matching_response, 'sortings': sortings})
        self.assertEqual(response.status_code, 200)

