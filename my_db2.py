import os
import django
import csv
import sys

from random import randint

from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airbitnbyte.settings")
django.setup()

from user.models import User,Bookmark
from property.models import (
    Property,
    PropertyImage,
    Host,
    Attribute,
    PropertyAttributes,
    Refund,
    Size,
    PropertySizes,
    Facility,
    PropertyFacilities,
    Safety,
    PropertySafeties,
    Rule,
    PropertyRules,
    Comment,
    Country,
    Province,
    City,
    District,
    Type,
    Category,
    Review
)

#fake = Faker('ko_KR')
#for i in range(1000):
#    User.objects.create(
#        email        = fake.email(),
#        birthday     = fake.date_of_birth(),
#        image_url    = fake.image_url(),
#        family_name  = fake.first_name(),
#        given_name   = fake.last_name(),
#        password     = fake.password())


for i in range(1,1000):
    Bookmark.objects.create(
        user_id =  i,
        property_id  = randint(1, 1000))

