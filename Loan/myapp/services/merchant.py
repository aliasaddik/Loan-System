from Loan.myapp.models.merchants import Merchant

def get_merchant_by_id(id: str) -> Merchant:
    """Return merchant who have the same id"""
    try:
        return Merchant.objects.get(id=int(id))
    except Merchant.DoesNotExist:
        return None