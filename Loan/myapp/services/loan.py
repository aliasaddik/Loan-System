from Loan.myapp.models.loans import MyLoan
from django.db.models import Sum



    
def get_loan_by_customer_id(id: str) -> MyLoan:
    """Return all loans for specific customer"""
    return MyLoan.objects.filter(customer__id=int(id))

def get_all_loans() -> MyLoan:
    """Return all loans"""
    return MyLoan.objects.all()

 

def no_of_loans() -> int:
    """Return number of loans"""
    return MyLoan.objects.count()

def total_money() -> float:
    "Return the total of accepted amount of the loan"
    return MyLoan.objects.filter(accepted=True).aggregate (Sum('accepted_amount'))['accepted_amount__sum']

def get_loan_by_id(id: str) -> MyLoan:
    """Return loan with the given id"""
    try:
        return MyLoan.objects.get(id=int(id))
    except MyLoan.DoesNotExist:
        return None
     