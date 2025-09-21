from django.contrib import admin

# Register your models here.
from ecomapp.models import Dummy
from ecomapp.models import faq
from ecomapp.models import Category,products
from ecomapp.models import *

admin.site.register(Dummy)
admin.site.register(faq)
admin.site.register(Category)
admin.site.register(products)
admin.site.register(Mycontact)
admin.site.register(Register1)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Payment)

admin.site.register(ShippingAddress)
