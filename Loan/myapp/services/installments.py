from Loan.myapp.models.customers import Customer
from Loan.myapp.models.loans import Installments
from django.db.models import Sum


def get_installment_by_customer_id(id:str) -> Installments:
    """Return installments of a specific user"""
    return Installments.objects.filter(loan__customer__id=int(id))

def get_installment_by_id(id:str) -> Installments:
    """Return installment with the given id"""
    try:
        return Installments.objects.get(id=int(id))
    except Installments.DoesNotExist:
        return None
    
 

def total_paid() -> float:
    "Return the total of amount of the paid installments"
    total_amount = Installments.objects.filter(paid=True).aggregate(Sum('amount_paid'))['amount_paid__sum']
    return total_amount or 0.0

     