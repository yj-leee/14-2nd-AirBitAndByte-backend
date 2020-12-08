from django.db   import models

from user.models import TimeStampedModel


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'types'

    def __str__(self):
        return self.name


class Property(TimeStampedModel):
    title           = models.CharField(max_length=100)
    content         = models.TextField()
    capacity        = models.IntegerField()
    price           = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_guest = models.DecimalField(max_digits=12, decimal_places=3)
    longitude       = models.DecimalField(max_digits=10, decimal_places=6)
    latitude        = models.DecimalField(max_digits=10, decimal_places=6)
    type            = models.ForeignKey('Type', on_delete=models.CASCADE, null=True)
    category        = models.ForeignKey('Category', on_delete=models.CASCADE)
    host            = models.ForeignKey('Host', on_delete=models.CASCADE)
    refund          = models.ForeignKey('Refund', on_delete=models.CASCADE)
    country         = models.ForeignKey('Country', on_delete=models.CASCADE)
    province        = models.ForeignKey('Province', on_delete=models.CASCADE)
    city            = models.ForeignKey('City', on_delete=models.CASCADE)
    district        = models.ForeignKey('District', on_delete=models.CASCADE)
    street          = models.CharField(max_length=1000)
    size            = models.ManyToManyField('Size', through='PropertySizes')
    attribute       = models.ManyToManyField('Attribute', through='PropertyAttributes')
    facility        = models.ManyToManyField('Facility', through='PropertyFacilities')
    rule            = models.ManyToManyField('Rule', through='PropertyRules')
    safety          = models.ManyToManyField('Safety', through='PropertySafeties')


    class Meta:
        db_table = 'properties'

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    url      = models.URLField(max_length=1000)

    class Meta:
        db_table = 'property_images'


class Host(TimeStampedModel):
    name     = models.CharField(max_length=100)
    is_super = models.BooleanField(null=True)

    class Meta:
        db_table = 'hosts'

    def __str__(self):
        return self.name


class Attribute(models.Model):
    title   = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = 'attributes'


class PropertyAttributes(models.Model):
    property  = models.ForeignKey('Property', on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    class Meta:
        db_table = 'property_attributes'


class Refund(models.Model):
    content = models.TextField()

    class Meta:
        db_table = 'refunds'


class Size(models.Model):
    name    = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name


class PropertySizes(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    size     = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'property_sizes'


class Facility(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'facilities'

    def __str__(self):
        return self.name


class PropertyFacilities(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    facility = models.ForeignKey('Facility', on_delete=models.CASCADE)

    class Meta:
        db_table = 'property_facilities'


class Review(TimeStampedModel):
    user          = models.ForeignKey('user.User', on_delete=models.CASCADE)
    property      = models.ForeignKey('Property', on_delete=models.CASCADE)
    content       = models.TextField()
    cleanliness   = models.DecimalField(max_digits=3, decimal_places=2)
    communication = models.DecimalField(max_digits=3, decimal_places=2)
    check_in      = models.DecimalField(max_digits=3, decimal_places=2)
    accuracy      = models.DecimalField(max_digits=3, decimal_places=2)
    location      = models.DecimalField(max_digits=3, decimal_places=2)
    affordability = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'reviews'


class Safety(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'safeties'

    def __str__(self):
        return self.name


class PropertySafeties(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    safety   = models.ForeignKey('Safety', on_delete=models.CASCADE)

    class Meta:
        db_table = 'property_safeties'


class Rule(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'rules'

    def __str__(self):
        return self.name


class PropertyRules(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    rule     = models.ForeignKey('Rule', on_delete=models.CASCADE)

    class Meta:
        db_table = 'property_rules'


class Comment(TimeStampedModel):
    review  = models.ForeignKey('Review', on_delete=models.CASCADE)
    host    = models.ForeignKey('Host', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = 'comments'


class Country(models.Model):
    name       = models.CharField(max_length=200)
    latitude   = models.DecimalField(max_digits=10, decimal_places=6)
    longitude  = models.DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        db_table  = 'countries'

    def __str__(self):
        return self.name


class Province(models.Model):
    name       = models.CharField(max_length=200)
    latitude   = models.DecimalField(max_digits=10, decimal_places=6)
    longitude  = models.DecimalField(max_digits=10, decimal_places=6)
    country    = models.ForeignKey('Country', on_delete=models.CASCADE)

    class Meta:
        db_table  = 'provinces'

    def __str__(self):
        return self.name


class City(models.Model):
    name       = models.CharField(max_length=200)
    latitude   = models.DecimalField(max_digits=10, decimal_places=6)
    longitude  = models.DecimalField(max_digits=10, decimal_places=6)
    province   = models.ForeignKey('Province', on_delete=models.CASCADE)

    class Meta:
        db_table  = 'cities'

    def __str__(self):
        return self.name


class District(models.Model):
    name       = models.CharField(max_length=200)
    latitude   = models.DecimalField(max_digits=10, decimal_places=6)
    longitude  = models.DecimalField(max_digits=10, decimal_places=6)
    city       = models.ForeignKey('City', on_delete=models.CASCADE)

    class Meta:
        db_table  = 'districts'

    def __str__(self):
        return self.name