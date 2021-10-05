from django.contrib import admin

from basket.admin import BasketAdmin
from basket.models import Basket
from .models import User

# Register your models here.


# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)
