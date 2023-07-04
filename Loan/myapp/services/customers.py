from Loan.myapp.models.customers import Customer
def get_customer_by_email(email: str) -> Customer:
    """Return customer who have this email"""
    try:
        return Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return None
def get_customer_by_usercode(usercode: str) -> Customer:
    """Return customer who have this usercode"""
    try:
        return Customer.objects.get(usercode=usercode)
    except Customer.DoesNotExist:
        return None
def get_customer_by_id(id: str) -> Customer:
    """Return customer who have the same id"""
    try:
        return Customer.objects.get(id=int(id))
    except Customer.DoesNotExist:
        return None
    
def get_all_customers() -> Customer:
    """Return all customers"""
    return Customer.objects.all()