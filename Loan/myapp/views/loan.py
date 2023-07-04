import csv
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from Loan.myapp.api.permission import IsAdmin, IsCustomer, IsMerchant
from Loan.myapp.api.response import CustomResponse
from Loan.myapp.models.loans import MyLoan
from Loan.myapp.serializers.loan import LoanGetSerializer, LoanSerializer, LoanStatsSerializer
from Loan.myapp.services.installments import total_paid
from Loan.myapp.services.loan import get_all_loans, get_loan_by_customer_id, get_loan_by_id, no_of_loans, total_money
from Loan.myapp.utils.csvgen import generate_csv_response

class LoanCreateAPIView(GenericAPIView):
    serializer_class = LoanSerializer
    permission_classes = (IsMerchant, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success( message="Loan created successfully")
        return CustomResponse.bad_request(error=serializer.errors)
    
class LoanCustomerAPIView(ListAPIView):
    permission_classes = (IsCustomer,)
    serializer_class = LoanGetSerializer

    def get_queryset(self):
        """get all loans of a specific user"""
        query_set = get_loan_by_customer_id(self.request.user.id)
        return query_set
    
class LoanAdminAPIView(ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = LoanGetSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['business', 'customer', 'no_of_months','accepted_amount','total_amount','interest_rate', 'accepted']
    ordering_fields = ['business', 'customer', 'no_of_months','accepted_amount','total_amount','interest_rate',  ]
    
    def get_queryset(self):
        
        query_set = MyLoan.objects.all() 
 
        return query_set
    
class LoanCSVDownloadAPIView(GenericAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = LoanGetSerializer
   
    def get(self, request):
        header_row = ['Business', 'Customer', 'No. of Months', 'Accepted Amount', 'Total Amount', 'Interest Rate', 'Created At', 'Requested Amount', "Accepted"]
        field_names = ['business', 'customer', 'no_of_months', 'accepted_amount', 'total_amount', 'interest_rate', 'created_at', 'requested_amount', 'accepted']
        return generate_csv_response(MyLoan.objects.all(), "alldata", header_row, field_names)

       

class LoanByIdAPIView(GenericAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = LoanGetSerializer
    def get(self, request, id: str):
        """To get a loan by id"""
        loan = get_loan_by_id(id)
        if loan is not None:
            serializer = self.get_serializer(loan)
            return CustomResponse.success(data=serializer.data)
        return CustomResponse.not_found(status_code=404, message="loan not found")
    
class LoanRejectAPIView(GenericAPIView):
   
    serializer_class = LoanGetSerializer
    permission_classes = (IsCustomer,)
    def delete(self, request,id: str):
        """To delete a user"""
        loan = get_loan_by_id(id)
        if loan is not None:
            loan.delete()
            return CustomResponse.success(message="Loan rejected")
        return CustomResponse.not_found(message="loan not found")
    

class LoanStatsAPIView(GenericAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = LoanStatsSerializer
    def get(self, request):
         
        loans_count = no_of_loans()
        total_money_value = total_money()
        total_paid_value = total_paid()

          
        data = {
            'no_of_loans': loans_count,
            'total_money': total_money_value,
            'total_paid': total_paid_value
        }

       
        serializer = LoanStatsSerializer(data)

    
        return CustomResponse.success(data=serializer.data)
       