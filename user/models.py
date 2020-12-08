from django.db import models

class TimeStampedModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)

     class Meta:
         abstract = True


class User(TimeStampedModel):
    email        = models.EmailField()
    birthday     = models.DateField(auto_now_add=False, null=True)
    image_url    = models.URLField(max_length=1000, null=True)
    given_name   = models.CharField(max_length=200, null=True)
    family_name  = models.CharField(max_length=200, null=True)
    password     = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


class Bookmark(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookmarks'