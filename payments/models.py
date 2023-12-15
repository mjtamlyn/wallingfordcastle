from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Checkout(models.Model):
    stripe_id = models.CharField(max_length=128)
    user = models.ForeignKey('wallingford_castle.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.stripe_id

    def mark_as_paid(self):
        for item in self.lineitemintent_set.all():
            item.item.paid = True
            item.item.save()


class LineItemIntent(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Line item for %s' % self.item
