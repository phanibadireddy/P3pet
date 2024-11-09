from django.contrib import admin
from .models import register,ads,pay,Purchase,Address,DeliveryRequest,complaints

admin.site.register(register)
admin.site.register(ads)
admin.site.register(pay)
admin.site.register(Purchase)
admin.site.register(Address)
admin.site.register(DeliveryRequest)
admin.site.register(complaints)