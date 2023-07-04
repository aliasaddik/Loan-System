from rest_framework.generics import GenericAPIView, ListAPIView
from Loan.myapp.api.permission import IsCustomer
from Loan.myapp.models.loans import Installments
from Loan.myapp.serializers.installments import InstallmentCreateSerializer, InstallmentSerializer
from Loan.myapp.services.installments import get_installment_by_customer_id, get_installment_by_id
from Loan.myapp.services.loan import get_loan_by_id
from datetime import datetime, timedelta
from Loan.myapp.api.response import CustomResponse
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta

class InstallmentsAPIView(GenericAPIView):
    "Api View to accept the loan and create all its installments objects"
    serializer_class = InstallmentCreateSerializer
    permission_classes = (IsCustomer,)
    def post(self, request,  id: str):
        loan = get_loan_by_id(id)
        if loan:
            if not loan.accepted == True:
                loan.accepted = True
                loan.save()

                # Create installments with the number of months
                installments_created = []
                current_date = datetime.now().date()  
                no_of_months = loan.no_of_months
                original_amount_due = loan.total_amount/no_of_months
                amount_without_interest = loan.accepted_amount/no_of_months

                for month in range(0,no_of_months):
                   
                   due_date = current_date + relativedelta(months=month)
                   installment = Installments(
                      loan=loan,
                      original_amount_due=original_amount_due,
                      amount_without_interest = amount_without_interest,
                      due_date=due_date)
                   installment.save()
                   installments_created.append(installment)


                serializer = InstallmentCreateSerializer(installments_created, many=True)
                serialized_installments = serializer.data
                return CustomResponse.success(data= serialized_installments, message="Loan accepted successfully")
            return CustomResponse.bad_request(message= "Loan already accepted")
        return CustomResponse.bad_request(message= "Loan not found")
    def put(self, request,  id: str):
        installment = get_installment_by_id(id)

        if installment:
            if not installment.paid:
                if installment.loan.customer.id == request.user.id:
                    installment.amount_paid = installment.get_amount_to_pay
                    installment.paid = True

                    installment.save()
                    return CustomResponse.success(message="Installment paid successfully")
                return CustomResponse.bad_request(message= "You are not the owner of this installment")
            return CustomResponse.bad_request(message= "Installment already paid")
        return CustomResponse.bad_request(message= "Installment not found")
                


    
class CustomerInstallmentAPIView(ListAPIView):
    serializer_class = InstallmentSerializer
    permission_classes = (IsCustomer,)

    def get_queryset(self) -> Response:
        """get all installments of a specific user"""
        query_set = get_installment_by_customer_id(self.request.user.id)
        return query_set  
        


