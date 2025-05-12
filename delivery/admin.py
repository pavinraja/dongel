from django.contrib import admin
from .models import user, Restaurant, Item, Cart

# Register your models here.
admin.site.register(user)
admin.site.register(Restaurant)
admin.site.register(Item)

admin.site.register(Cart)

