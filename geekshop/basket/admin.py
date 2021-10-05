from django.contrib import admin

# Register your models here.
from basket.models import Basket


admin.site.register(Basket)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp', 'updated_timestamp')
    readonly_fields = ('created_timestamp', 'updated_timestamp')
    extra = 0
