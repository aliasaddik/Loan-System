from django.utils import timezone
from django.db import models
from Loan.myapp.models.merchants import Business
from Loan.myapp.models.customers import Customer
from django.contrib import admin

def upload_to(instance, filename):
    return 'pdfs/{filename}'.format(filename=filename)

class MyLoan (models.Model):
    business = models.ForeignKey(Business, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    requested_amount = models.IntegerField()
    accepted_amount = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    #total amount to pay with interest based on the number of months
    total_amount =  models.IntegerField()
    no_of_months = models.IntegerField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    offer_pdf = models.FileField(upload_to=upload_to)
    
    
class Installments(models.Model):
    accepted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    loan = models.ForeignKey(MyLoan, on_delete = models.CASCADE)
    due_date = models.DateField()
    amount_without_interest = models.DecimalField(max_digits=8, decimal_places=2)
    original_amount_due= models.DecimalField(max_digits=8, decimal_places=2)
    paid= models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
   

    @property
    def get_over_due(self):
        if self.due_date < timezone.now().date():
            return True
        return False    
    @property
    def get_amount_to_pay(self):
        int 
        if self.paid:
            return 0
        if self.due_date > timezone.now().date():
            return self.original_amount_due
        else:
            no_of_days = (timezone.now().date() - self.due_date).days;
            return self.original_amount_due * no_of_days *(self.loan.business.late_fee_interest+100)
admin.site.register(MyLoan) 
admin.site.register(Installments) 