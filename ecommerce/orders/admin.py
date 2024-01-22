from django.contrib import admin

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# register OrderAdmin here
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 
    'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'updated', 'created']
    inlines = [OrderItemInline]
# display: id, firstname, lastname, email, address, postal, city, paid, created time, updated time
# can filter with: paid, created time, updated time
# inline: OrderItemInline as above
