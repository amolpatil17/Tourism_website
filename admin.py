from django.contrib import admin
from .models import Payment, TouristInfo
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):         # this is for to show this data in django admin
    list_display = ("card_no","cvv","expiry","balance")

class TouristInfoAdmin(admin.ModelAdmin):
    list_display=("user_name","place_name","tour_price","total_price","total_persons","booked_date")

admin.site.register(Payment,PaymentAdmin)               #to add models to django admin register here
admin.site.register(TouristInfo,TouristInfoAdmin)



