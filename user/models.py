from django.db import models

class User(models.Model):
    email        = models.EmailField()
    phone_number = models.CharField(max_length=200)
    image_url    = models.URLField(max_length=1000, null=True)
    first_name   = models.CharField(max_length=200)
    last_name    = models.CharField(max_length=200)
    password     = models.CharField(max_length=1000)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
