from django.contrib import admin

# Register your models here.
from Home.models import *
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Orderdetail)
admin.site.register(Product)
admin.site.register(Usercart)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(Voucher)
#Tai khoan admin: admin, 10022002