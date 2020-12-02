from django.db import models

class TimeStampedModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)

     class Meta:
         abstract = True


class User(TimeStampedModel):
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


class Bookmark(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookmarks'
