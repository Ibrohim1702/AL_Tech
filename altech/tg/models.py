from django.db import models

# Create your models here.
from django.utils.text import slugify


class Log(models.Model):
    user_id = models.BigIntegerField()
    messages = models.JSONField(default={'state': 0})


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=128, null=True)
    # last_name = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=15, null=True)
    til = models.CharField(max_length=128, null=True)


class Catalog(models.Model):

    content = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content)
        return super(Catalog, self).save(*args, **kwargs)

    def __str__(self):
        return self.content


class Subcategory(models.Model):
    content = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)
    ctg = models.ForeignKey(Catalog, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content)
        return super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.content


class Brand(models.Model):
    content = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content)
        return super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.content


class Product(models.Model):
    name = models.CharField(max_length=128)
    characteristics = models.TextField()
    price = models.IntegerField()
    img = models.ImageField()
    ctg = models.ForeignKey(Catalog, on_delete=models.SET_NULL, null=True)
    subctg = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)


class Savat(models.Model):
    user_id = models.IntegerField()
    product = models.CharField(max_length=128)
    price = models.IntegerField()
    dona = models.IntegerField()
    slug = models.SlugField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product)
        return super(Savat, self).save(*args, **kwargs)

    def __str__(self):
        return self.product
