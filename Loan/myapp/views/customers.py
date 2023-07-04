from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView
from Loan.myapp.api.permission import IsAdmin
from Loan.myapp.api.response import CustomResponse
from Loan.myapp.serializers.customers import CustomerSerializer
from Loan.myapp.services.customers import get_all_customers, get_customer_by_id
from Loan.myapp.utils.csvgen import generate_csv_response


class AdminCustomerAPIView(GenericAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = CustomerSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["first_name","last_name", "email", "mobile_number", "date_of_birth",
    "current_debt_outside", "credit_limit_outside", "credit_history_length", "pursuit_of_new_credit",
    "months_since_last_late_payment", "credit_mix", "created_at"]
    ordering_fields = ["first_name","last_name", "email", "mobile_number", "date_of_birth",
    "current_debt_outside", "credit_limit_outside", "credit_history_length", "pursuit_of_new_credit",
    "months_since_last_late_payment", "credit_mix", "created_at"]
    def get(self, request, id: str):
        """To get a customer by id"""
        customer = get_customer_by_id(id)
        if customer is not None:
            serializer = self.get_serializer(customer)
            return CustomResponse.success(data=serializer.data)
        return CustomResponse.not_found(status_code=404, message="customer not found")
    
class AdminCustomerListAPIView(ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = CustomerSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields =["first_name","last_name", "email", "mobile_number", "date_of_birth",
    "current_debt_outside", "credit_limit_outside", "credit_history_length", "pursuit_of_new_credit",
    "months_since_last_late_payment", "credit_mix", "created_at"]
    ordering_fields =["first_name","last_name", "email", "mobile_number", "date_of_birth",
    "current_debt_outside", "credit_limit_outside", "credit_history_length", "pursuit_of_new_credit",
    "months_since_last_late_payment", "credit_mix", "created_at"]
    def get_queryset(self):
        """get all customers in the system"""
        query_set = get_all_customers()
        if 'download_csv' in self.request.query_params:
            header_row = ["First Name", "Last Name","Email","Mobile Number","Date of Birth",
              "Current Debt Outside","Credit Limit Outside","Credit History Length","Pursuit of New Credit",
              "Months Since Last Late Payment","Credit Mix","Created At"]
            field_names = ["first_name","last_name", "email", "mobile_number", "date_of_birth",
             "current_debt_outside", "credit_limit_outside", "credit_history_length", "pursuit_of_new_credit",
             "months_since_last_late_payment", "credit_mix", "created_at"]
            return generate_csv_response(query_set, "Customer", header_row, field_names)
        return query_set
    