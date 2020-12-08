import json
import jwt

from django.test     import TestCase, Client

from user.models     import User, Bookmark
from property.models import Property, Category, Host, Refund, Country, Province, City, District

client = Client()

class RegisterTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            email       = 'amusesla@gmail.com',
            password    = 'testing_exsiting_user',
            birthday    = '2000-02-06',
            given_name  = 'Giyong',
            family_name = 'Gim'
        )
    def tearDown(self):
        User.objects.all().delete()

    def test_register_user_success(self):

        data = {
            "email"         : "amuse@gmail.com",
            "password"      : "wecode!",
            "birthdayYear"  : "2000",
            "birthdayMonth" : "2",
            "birthdayDate"  : "6",
            "givenName"     : "Giyong",
            "familyName"    : "Gim"
    }
        response = client.post('/register', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_register_user_already_exist(self):

        data2 = {
            "email"         : "amusesla@gmail.com",
            "password"      : "wecode!",
            "birthdayYear"  : "2000",
            "birthdayMonth" : "2",
            "birthdayDate"  : "6",
            "givenName"     : "Giyong",
            "familyName"    : "Gim"
        }
        response = client.post('/register', json.dumps(data2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_key(self):

        data3 = {
            "email"         : "amuse@gmail.com",
            "password"      : "wecode!",
            "birthdayYear"  : "2000",
            "birthdayMonth" : "2",
            "birthdayDay"   : "6",
            "givenName"     : "Giyong",
            "familyName"    : "Gim"
        }
        response = client.post('/register', json.dumps(data3), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'KeyError'
                         }
                         )

class LoginTestCase(TestCase):

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
        client.post('/register', json.dumps(data), content_type='application/json')

    def test_login_success(self):
        data = {
            "email"    : "amusesla@gmail.com",
            "password" : "wecode!"
        }

        response = client.post('/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):
        data = {
            "email"    : "amusesla@gmail.com",
            "password" : "codestate!"
        }
        response = client.post('/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'Invalid_user'
                         }
                         )

    def test_login_keyError(self):
        data = {
            "email"    : "amusesla@gmail.com",
            "passward" : "codestate!"
        }
        response = client.post('/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'KeyError'
                         }
                         )

class BookmarkTestCase(TestCase):
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
        country  = Country.objects.create(name   = '성보', longitude = 1, latitude = 1)
        province = Province.objects.create(name  = '성보', longitude = 1, latitude = 1, country  = country)
        city     = City.objects.create(name      = '성보', longitude = 1, latitude = 1, province = province)
        district = District.objects.create(name  = '성보', longitude = 1, latitude = 1, city     = city)
        refund   = Refund.objects.create(content = '성보')
        host     = Host.objects.create(name      = '성보')
        category = Category.objects.create(name  = 'wow')
        property = Property.objects.create(title = '성보의하루',
                                           capacity         = 1,
                                           price            = 1,
                                           price_per_guest  = 1,
                                           longitude        = 1,
                                           latitude         = 1,
                                           category_id      = category.id,
                                           host_id          = host.id,
                                           refund_id        = refund.id,
                                           country_id       = country.id,
                                           province_id      = province.id,
                                           city_id          = city.id,
                                           district_id      = district.id,
                                           street           = '성보의길')

        client.post('/register', json.dumps(data), content_type='application/json')
        response = client.post('/login', json.dumps(data2), content_type='application/json')
        self.token = json.loads(response.content)['accessToken']

    def tearDown(self):

        Bookmark.objects.all().delete()

        Property.objects.all().delete()

        Country .objects.all().delete()

        Province.objects.all().delete()
        City    .objects.all().delete()
        District.objects.all().delete()
        Refund  .objects.all().delete()
        Host    .objects.all().delete()
        Category.objects.all().delete()
        User    .objects.all().delete()

#    def test_bookmark_create_success(self):
#
#        headers = {'HTTP_Authorization':self.token}
#        data = {
#            "propertyId" : 1
#        }
#        response = client.post('/bookmark', json.dumps(data), content_type='application/json', **headers)
#        self.assertEqual(response.status_code, 200)
#
#    def test_bookmark_create_fail(self):
#        data = {
#            "propertyId" : 1
#        }
#        response = client.post('/bookmark', json.dumps(data), content_type='application/json')
#        self.assertEqual(response.status_code, 400)
