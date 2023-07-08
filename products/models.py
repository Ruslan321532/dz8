from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=36)


class Product(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)

    @property
    def categories_list(self) -> list:
        return self.categories.all()
