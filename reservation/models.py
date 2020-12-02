import uuid

from django.db import models
from user.models import TimeStampedModel

class Reservation(TimeStampedModel):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    property  = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    check_in  = models.DateTimeField(auto_now_add=False)
    check_out = models.DateTimeField(auto_now_add=False)
    size      = models.ForeignKey('property.Size', on_delete=models.CASCADE)
    status    = models.ForeignKey('Status', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'


class Status(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'status'

    def __str__(self):
        return self.name



class Payment(TimeStampedModel):
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
    reservation    = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('Payment_method', on_delete=models.CASCADE)
    uuid           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status         = models.ForeignKey('Status', on_delete=models.CASCADE)

    class Meta:
        db_table = 'payments'


class PaymentMethod(TimeStampedModel):
    card_number = models.CharField(max_length=200)
    expire_date = models.DateTimeField(auto_now_add=False)
    card_holder = models.CharField(max_length=200)
    cvc         = models.CharField(max_length=200)

    class Meta:
        db_table = 'payment_method'
