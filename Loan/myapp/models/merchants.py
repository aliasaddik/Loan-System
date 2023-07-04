from django.db import models
from Loan.myapp.models.users import MyUser
from django.contrib import admin

class Field(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
    

class Business(models.Model):
    name = models.CharField(max_length=45)
    field = models.ForeignKey(Field, on_delete = models.CASCADE)
    late_fee_interest = models.DecimalField(max_digits=5, decimal_places=2)
    base_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    lending_starting_range = models.IntegerField()
    lending_end_range = models.IntegerField()
    def __str__(self) -> str:
        return self.name
    
    
 

class Merchant (MyUser):
    business = models.ForeignKey(Business, on_delete = models.CASCADE)
admin.site.register(Field)
admin.site.register(Business)
admin.site.register(Merchant)