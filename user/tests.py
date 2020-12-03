import json
import jwt

from django.test     import TestCase, Client

from user.models     import User

client = Client()


class RegisterTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            email       = 'amusesla@gmail.com',
            password    = 'wecode!',
            birthday    = '2000-02-06',
            given_name  = 'Giyong',
            family_name = 'Gim'
        )

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
        self.assertEqual(response.json(),
                         {
                             'message':'User_already_exist'
                         }
                         )

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
