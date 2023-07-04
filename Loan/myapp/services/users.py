
from Loan.myapp.models.users import MyUser

def get_user_by_email(email: str) -> MyUser:
    """Return user who have this email"""
    try:
        return MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return None
def get_user_by_id(id: str) -> MyUser:
    """Return user who have the same id"""
    try:
        return MyUser.objects.get(id=int(id))
    except MyUser.DoesNotExist:
        return None

def get_user_type_by_id(id: str) -> MyUser:
    """Return user type by id"""
    try:
        user = MyUser.objects.get(id=int(id))
        return user.user_type
    except MyUser.DoesNotExist:
        return None
