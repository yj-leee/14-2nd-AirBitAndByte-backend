import json
import jwt

from django.test        import TestCase, Client

from user.models        import User, Bookmark
from property.models    import Property, Category, Host, Refund, Country, Province, City, District, Size
from reservation.models import Status, Reservation

client = Client()

class ReservationTestCase(TestCase):

    def setUp(self):
        data = {
            "email"         : "amusesla@gmail.com",
            "password"      : "wecode!",
            "birthdayYear"  : "2000",
            "birthdayMonth" : "2",
            "birthdayDate"  : "6",
            "givenName"     : "Giyong",
            "familyName"    : "Gim"
        }

        data2 = {
            "email"    : "amusesla@gmail.com",
            "password" : "wecode!"
        }
        user     = User.objects.create(email    = 'seungbo@gmail.com',
                                       password = 'seungbo',)
        country  = Country.objects.create(name   = '성보', longitude = 1, latitude = 1)
        province = Province.objects.create(name  = '성보', longitude = 1, latitude = 1, country  = country)
        city     = City.objects.create(name      = '성보', longitude = 1, latitude = 1, province = province)
        district = District.objects.create(name  = '성보', longitude = 1, latitude = 1, city     = city)
        refund   = Refund.objects.create(content = '성보')
        host     = Host.objects.create(name      = '성보')
        size     = Size.objects.create(name      = '성보', content='성보')
        status   = Status.objects.create(name    = '성보')
        category = Category.objects.create(name  = 'wow')
        property = Property.objects.create(title = '성보의하루',
                                capacity         = 1,
                                price            = 1,
                                price_per_guest  = 1,
                                longitude        = 1,
                                latitude         = 1,
                                category         = category,
                                host             = host,
                                refund           = refund,
                                country          = country,
                                province         = province,
                                city             = city,
                                district         = district)
        print('property_id:', property.id)
        reservation = Reservation.objects.create(check_in    = '2020-01-10',
                                                 check_out   = '2020-01-20',
                                                 property_id = property.id,
                                                 size_id     = size.id,
                                                 status_id   = status.id,
                                                 user_id     = user.id)
        print('reservation_id', reservation.id)



        client.post('/register', json.dumps(data), content_type='application/json')
        response = client.post('/login', json.dumps(data2), content_type='application/json')
        self.token = json.loads(response.content)['accessToken']

    def tearDown(self):
        Bookmark.objects.all().delete()
        Country .objects.all().delete()
        Province.objects.all().delete()
        City    .objects.all().delete()
        District.objects.all().delete()
        Refund  .objects.all().delete()
        Host    .objects.all().delete()
        Category.objects.all().delete()
        User    .objects.all().delete()
        Property.objects.all().delete()
        Property.objects.all().delete()
        Reservation.objects.all().delete()

    def test_reservation_list(self):
        headers  = {'HTTP_Authorization': self.token}
        response = client.get('/reservation', **headers)
        self.assertEqual(response.status_code, 200)

    def test_reservation_list_fail_without_token(self):
        response = client.get('/reservation')
        self.assertEqual(response.status_code, 400)

    def test_reservation_create(self):
        headers = {'HTTP_Authorization':self.token}
        data= {
            "propertyId" : "1",
            "checkIn"    : "2020-01-19",
            "checkOut"   : "2020-01-20",
            "sizeId"     : "1",
            "statusId"   : "1"
        }

        response = client.post('/reservation', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_reservation_create_fail_without_token(self):
        data= {
            "propertyId" : "1",
            "checkIn"    : "2020-01-19",
            "checkOut"   : "2020-01-20",
            "sizeId"     : "1",
            "statusId"   : "1"
        }

        response = client.post('/reservation', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'Invalid_user'
                         }
                         )

    def test_reservation_create_fail_same_input_date(self):
        headers = {'HTTP_Authorization':self.token}
        data= {
            "propertyId" : "1",
            "checkIn"    : "2020-01-19",
            "checkOut"   : "2020-01-19",
            "sizeId"     : "1",
            "statusId"   : "1"
        }
        response = client.post('/reservation', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'Not_Available'
                         }
                         )

class PaymentTestCase(TestCase):
    def setUp(self):
        data = {
            "email"         : "amusesla@gmail.com",
            "password"      : "wecode!",
            "birthdayYear"  : "2000",
            "birthdayMonth" : "2",
            "birthdayDate"  : "6",
            "givenName"     : "Giyong",
            "familyName"    : "Gim"
        }

        data2 = {
            "email"    : "amusesla@gmail.com",
            "password" : "wecode!"
        }
        user     = User.objects.create(email    = 'seungbo@gmail.com',
                                       password = 'seungbo',)
        country  = Country.objects.create(name   = '성보', longitude = 1, latitude = 1)
        province = Province.objects.create(name  = '성보', longitude = 1, latitude = 1, country  = country)
        city     = City.objects.create(name      = '성보', longitude = 1, latitude = 1, province = province)
        district = District.objects.create(name  = '성보', longitude = 1, latitude = 1, city     = city)
        refund   = Refund.objects.create(content = '성보')
        host     = Host.objects.create(name      = '성보')
        size     = Size.objects.create(name      = '성보', content='성보')
        status   = Status.objects.create(name    = '성보')
        category = Category.objects.create(name  = 'wow')
        property = Property.objects.create(title = '성보의하루',
                                capacity         = 1,
                                price            = 1,
                                price_per_guest  = 1,
                                longitude        = 1,
                                latitude         = 1,
                                category         = category,
                                host             = host,
                                refund           = refund,
                                country          = country,
                                province         = province,
                                city             = city,
                                district         = district)
        print('property_id:', property.id)
        reservation = Reservation.objects.create(check_in    = '2020-01-10',
                                                 check_out   = '2020-01-20',
                                                 property_id = property.id,
                                                 size_id     = size.id,
                                                 status_id   = status.id,
                                                 user_id     = user.id)
        print('reservation_id', reservation.id)



        client.post('/register', json.dumps(data), content_type='application/json')
        response = client.post('/login', json.dumps(data2), content_type='application/json')
        self.token = json.loads(response.content)['accessToken']

    def test_payment_sucess(self):
        headers = {'HTTP_Authorization':self.token}
        response = client.post('/reservation/1', **headers)
        self.assertEqual(response.status_code, 400)
