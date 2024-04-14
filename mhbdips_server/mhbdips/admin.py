from django.contrib import admin
from .models import Product, OrderDetail, Shipper, Invoice, Review,ContactMessage, Account

# Register your models here.
admin.site.register(Account)
admin.site.register(Product)
admin.site.register(OrderDetail)
admin.site.register(Shipper)
admin.site.register(Invoice)
admin.site.register(Review)
admin.site.register(ContactMessage)
