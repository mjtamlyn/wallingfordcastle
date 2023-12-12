from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Round(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    can_be_wrs = models.BooleanField(default=True)

    def __str__(self):
        return self.name
