import json
import jwt

from django.test     import TestCase, Client

from user.models     import User

client = Client()


class PropertyListTestCase(TestCase):

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

        response = client.post('/register', json.dumps(data), content_type='application/json')
        response = client.post('/login', json.dumps(data2), content_type='application/json')
        self.token = json.loads(response.content)['accessToken']


    def tearDown(self):
        User.objects.all().delete()

    def test_property_list_success(self):
        response = client.get('/property')
        self.assertEqual(response.status_code, 200)

    def test_property_list_success_with_valid_user(self):
        headers = {'HTTP_Authorization':self.token}
        response = client.get('/property')
        self.assertEqual(response.status_code, 200)

    def test_property_list_filter_success(self):
        response = client.get('/property?category=1&is_super=True&rule=7&check_in=2020-01-01&check_out=2020-01-10&guest=6&search=제주')
        self.assertEqual(response.status_code, 200)

    def test_property_list_filter_success_with_valid_user(self):
        headers = {'HTTP_Authorization':self.token}
        response = client.get('/property')
        self.assertEqual(response.status_code, 200)

    def test_property_list_filter_invalid_date(self):
        response = client.get('/property?check_in=2020-01-20&check_out=2020-01-10')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'Invalid_date'
                         }
                         )
    def test_property_list_invalid_date_format(self):
        response = client.get('/property?check_in=2020-000')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'message':'Invalid_date_format'
                         }
                         )
