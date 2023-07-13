from django.contrib import admin
from .models import Catalog, Product, Savat, Brand, Subcategory
# Register your models here.
admin.site.register(Catalog)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Savat)
admin.site.register(Subcategory)