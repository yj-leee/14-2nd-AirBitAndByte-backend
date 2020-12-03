import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airbitnbyte.settings")
django.setup()

from user.models import User
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
    Review,
    Safety,
    PropertySafeties,
    Rule,
    PropertyRules,
    Comment,
    Country,
    Province,
    City,
    District,
    Street,
    Type,
    Category
)


# User
User.objects.create(email='amusesla@gmail.com', family_name='Gim', given_name='Giyong', password='wecode!', birthday='2000-02-06')




CSV_PATH_PRODUCTS = './categories.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Category.objects.create(name = row[0])


CSV_PATH_PRODUCTS = './attributes.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        title    = row[0]
        content  = row[1]

        Attribute.objects.create(
            title   = title,
            content = content
        )

#Refunds
CSV_PATH_PRODUCTS = './refunds.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        content = row[0]

        Refund.objects.create(
            content = content
        )

#Hosts
CSV_PATH_PRODUCTS = './hosts.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Host.objects.create(
            name = row[0],
            is_super = row[1]
        )

#Sizes
CSV_PATH_PRODUCTS = './sizes.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name     =  row[0]
        content  =  row[1]

        Size.objects.create(
            name     = name,
            content  = content
        )

#Facilities
CSV_PATH_PRODUCTS = './facilities.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]

        Facility.objects.create(
            name = name
        )

# Country
CSV_PATH_PRODUCTS = './countries.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        name = row[0]
        latitude = row[1]
        longitude = row[2]

        Country.objects.create(
            name       = name,
            latitude   = latitude,
            longitude  = longitude
        )

# Province
CSV_PATH_PRODUCTS = './provinces.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]
        country_id = row[1]
        latitude = row[2]
        longitube = row[3]

        Province.objects.create(
            name        = name,
            latitude    = latitude,
            longitude   = longitude,
            country_id  = country_id
        )

# City
CSV_PATH_PRODUCTS = './cities.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name         = row[0]
        province_id  = row[1]
        latitude     = row[2]
        longitude    = row[3]

        City.objects.create(
            name         = name,
            latitude     = latitude,
            longitude    = longitude,
            province_id  = province_id
        )

# District
CSV_PATH_PRODUCTS = './districts.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name       = row[0]
        city_id    = row[1]
        latitude   = row[2]
        longitude  = row[3]

        District.objects.create(
            name       = name,
            city_id    = city_id,
            latitude   = latitude,
            longitude  = longitude,
        )

# Rule
CSV_PATH_PRODUCTS = './rules.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        name = row[0]

        Rule.objects.create(name=name)

# Safety
CSV_PATH_PRODUCTS = './Safeties.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        name = row[0]

        Safety.objects.create(name = name)


# Types
CSV_PATH_PRODUCTS = './types.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        name = row[0]

        Type.objects.create(name = name)

# PROPERTY
CSV_PATH_PRODUCTS = 'property.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Property.objects.create(category_id=row[0], type_id=row[1], title=row[2], host_id=row[3], price=row[4], capacity=row[5], price_per_guest=row[6], latitude=row[7], longitude=row[8], refund_id=row[9], country_id=row[10], province_id=row[11], city_id=row[12], district_id=row[13], street=row[14], content=row[15])
 ##        type_id          = row[0]
 ##        title            = row[1]
 ##        host_id          = row[2]
 ##        price            = row[3]
 ##        capacity         = row[4]
 ##        price_per_guest  = row[5]
 ##        latitude         = row[6]
 ##        longitude        = row[7]
 ##        refund_id        = row[8]
 ##        country_id       = row[9]
 ##        province_id      = row[10]
 ##        city_id          = row[11]
 ##        district_id      = row[12]
 ##        street           = row[13]
 ##        content          = row[14]
 #
 ##        Property.objects.create(
 ##            title            = title,
 ##            content          = content,
 ##            capacity         = capacity,
 ##            price            = price,
 ##            price_per_guest  = price_per_guest,
 ##            longitude        = longitude,
 ##            latitude         = latitude,
 ##            type_id          = type_id,
 ##            host_id          = host_id,
 ##            refund_id        = refund_id,
 ##            country_id       = country_id,
 ##            province_id      = province_id,
 ##            city_id          = city_id,
 ##            district_id      = district_id,
 ##            street           = street
 ##        )
 #
#PROPERTY_IMAGE
CSV_PATH_PRODUCTS = './property_image.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        PropertyImage.objects.create(url=row[0], property_id=row[1])
#        url          = row[0]
#        property_id  = row[1]
#
#        PropertyImage.objects.create(
#            url       = url,
#            property_id  = property_id
#        )

#PROPERTY_ATTRIBUTE
CSV_PATH_PRODUCTS = './property_attribute.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        property_id   = row[0]
        attribute_id  = row[1]

        PropertyAttributes.objects.create(
            property_id  = property_id,
            attribute_id  = attribute_id
        )


#PROPERT_SIZES
CSV_PATH_PRODUCTS = './property_sizes.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        PropertySizes.objects.create(property_id = row[0], size_id = row[1])

#PROPERT_FACILITIES
CSV_PATH_PRODUCTS = './property_facilities.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        property_id = row[0]
        facility_id = row[1]

        PropertyFacilities.objects.create(
            property_id = property_id,
            facility_id = facility_id
        )

#REVIEWS - user doesn't exist
CSV_PATH_PRODUCTS = 'reviews.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        content        = row[0]
        cleanliness    = row[1]
        communication  = row[2]
        check_in       = row[3]
        accuracy       = row[4]
        location       = row[5]
        affordability  = row[6]
        user_id        = row[7]
        property_id    = row[8]

        Review.objects.create(
            user_id           = user_id,
            property_id       = property_id,
            content        = content,
            cleanliness    = cleanliness,
            communication  = communication,
            check_in       = check_in,
            accuracy       = accuracy,
            location       = location,
            affordability  = affordability
        )

# Comment
CSV_PATH_PRODUCTS = './comments.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        review_id  = row[0]
        host_id    = row[1]
        content    = row[2]

        Comment.objects.create(
            review_id  = review_id,
            host_id    = host_id,
            content    = content
        )

#property_rules
CSV_PATH_PRODUCTS = './property_rules.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        PropertyRules.objects.create(
            property_id  = row[0],
            rule_id      = row[1]
        )

#property_safeties
CSV_PATH_PRODUCTS = './property_safeties.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        PropertySafeties.objects.create(
            property_id  = row[0],
            safety_id    = row[1]
        )
