from django.db import models
from adminapp.models import Tourism
# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key=True)     # create user info for signup
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "UserInfo"

class Bookings(models.Model):
    user = models.ForeignKey(UserInfo,on_delete = models.CASCADE)  #userid
    tourism = models.ForeignKey(Tourism,on_delete=models.CASCADE)  #tourism id
    persons = models.IntegerField()

    class Meta:
        db_table = "Bookings"

class Payment(models.Model):
    card_no = models.CharField(max_length = 16)    # create table for input  values from tourist for payment
    expiry = models.CharField(max_length = 7)
    cvv = models.CharField(max_length = 3)
    balance = models.FloatField(default=10000)

    class Meta:
        db_table = "Payment"



class TouristInfo(models.Model):
    user_name=models.CharField(max_length=100)      # save info of tourist who have booked the tour
    place_name=models.CharField(max_length=100)
    tour_price=models.CharField(max_length=100)
    total_price=models.CharField(max_length=100,default=5)
    total_persons=models.CharField(max_length=50)
    booked_date=models.DateTimeField()


    class Meta:
        db_table="TouristInfo"