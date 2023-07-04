from django.utils import timezone
from datetime import datetime, timedelta
from unittest.util import _MAX_LENGTH
from Loan.myapp.models.users import MyUser
from django.db import models
from django.contrib import admin

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Customer(MyUser):
    id_front = models.ImageField(upload_to=upload_to)
    id_back = models.ImageField(upload_to=upload_to)
    date_of_birth = models.DateField()
    usercode= models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    current_debt_outside = models.IntegerField()
    credit_limit_outside = models.IntegerField()
    credit_history_length = models.IntegerField()
    pursuit_of_new_credit = models.IntegerField()
    months_since_last_late_payment = models.IntegerField()
    credit_mix = models.IntegerField()

    @property 
    def get_credit_limit(self):
        """
        Calculating in system credit limit based on the credit score [62 - 340] and limit ranging from 5k to 25k

        """
 
        credit_score = self.get_user_credit_score
        if credit_score < 118:
            limit = 5000
        elif credit_score < 174:
            limit = 10000
        elif credit_score < 229:
            limit = 15000
        elif credit_score < 285:
            limit = 20000
        else:
            limit = 25000
        return limit
    
    @property 
    def get_insystem_new_credit(self):
        """
        Get the number of loans the customer has accepted in the last 6 months
        """
        current_time = timezone.now()
        six_months_ago = current_time - timezone.timedelta(days=180)
        return self.myloan_set.filter(accepted=True, created_at__gte = six_months_ago).count()

   
    @property
    def get_months_since_most_recent_overdue(self):
        """
        Get the number of months since the most recent overdue payment
        """
        most_recent_overdue_loan = self.myloan_set.order_by('-installments__due_date').first()

        if most_recent_overdue_loan:
            most_recent_overdue_installment = None
            installments = most_recent_overdue_loan.installments_set.order_by('-due_date')

            for installment in installments:
                if installment.get_over_due:  # Assuming get_over_due is a property of the Installment model
                    most_recent_overdue_installment = installment
                    break

            if most_recent_overdue_installment:
              current_time = datetime.now()
              due_date = datetime.combine(most_recent_overdue_installment.due_date, datetime.min.time())
              time_difference = current_time - due_date
              months = time_difference.days // 30
              return months

        return -1
    @property 
    def get_current_outstanding_debt(self):
        """
        Get the amount of money the customer currently owes
        """
 
        amount = self.myloan_set.filter(installments__paid=False).aggregate(models.Sum('installments__amount_without_interest'))['installments__amount_without_interest__sum']
        if amount:
            return amount
        else: 
            return 0
    @property
    def get_insystem_credit_history_length(self):
         """
         Get the time in  months since the customer accepted their first loan in this system.
         """
         
         first_loan = self.myloan_set.filter(accepted=True).order_by('created_at').first()
         if first_loan:
            current_time = timezone.now()
            time_difference = current_time - first_loan.created_at
            months = time_difference.days // 30
            return months
         return 0

    @property
    def get_user_credit_score(self):
        'calculate the credit score of the customer based on the financial data and the credit history'
        credit_score = 0

        #checking if the customer latest late payment was inside or outside then determine credit score based on that
        if self.months_since_last_late_payment >= self.get_months_since_most_recent_overdue:
            months= self.months_since_last_late_payment
        else:
            months= self.get_months_since_most_recent_overdue
        if months <0:
            credit_score = 75
        elif months < 6:
            credit_score = 10
        elif months < 12:
            credit_score = 15
        elif months < 24:
            credit_score = 25
        else: 
            credit_score = 55
        

        #adding the credit score based on the debt to credit limit ratio
        if (self.credit_limit_outside == 0 and self.get_insystem_credit_history_length==0):
            ratio = 0.5
        elif (self.credit_limit_outside == 0 and self.get_insystem_credit_history_length>0):
            ratio = self.get_current_outstanding_debt / self.get_credit_limit
        elif (self.credit_limit_outside > 0 and self.get_insystem_credit_history_length==0):
            ratio = self.current_debt_outside / self.credit_limit_outside

        else:
            ratio = (self.get_current_outstanding_debt + self.current_debt_outside)/ (self.credit_limit_outside+self.get_credit_limit)

        if ratio < 0.3 :
            credit_score += 55
        elif ratio < 0.5:
            credit_score += 40
        elif ratio < 0.7:
            credit_score += 25
        elif ratio < 0.9:
            credit_score += 10
        else:
            credit_score += 5

        #adding the credit score based on the credit history length
        if self.credit_history_length==0 and self.get_insystem_credit_history_length>0:
            history= self.get_insystem_credit_history_length
        else:
           history = self.credit_history_length   

        if history < 12:
            credit_score += 12
        elif history < 24:
            credit_score += 35
        elif history < 48:
            credit_score += 60
        else: 
            credit_score += 75
        
        # adding the credit score based on the pursuit of new credit
        new_credit =  self.get_insystem_new_credit + self.pursuit_of_new_credit
        if new_credit == 0:
            credit_score += 75
        elif new_credit == 1:
            credit_score += 60
        elif new_credit == 2:
            credit_score += 45
        elif new_credit == 3:
            credit_score += 25
        else:
            credit_score += 20
        
        #adding the credit score based on the credit mix
        if self.credit_mix == 0:
            credit_score += 15
        elif self.credit_mix == 1:
            credit_score += 25
        elif self.credit_mix == 2:
            credit_score += 50
        elif self.credit_mix == 3:
            credit_score += 60
        else:
            credit_score += 50
        
        return credit_score
        
admin.site.register(Customer)                 

        
        


        
        

         

       

 




