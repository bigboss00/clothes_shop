from django.contrib import admin

from .models import Product, Favorite

admin.site.register([Product, Favorite])
