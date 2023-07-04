from rest_framework import serializers
from Loan.myapp.models.loans import Installments

class InstallmentSerializer(serializers.ModelSerializer):
    'Installment Serializer that can be used by the customer to view installments'
    amount_to_pay = serializers.SerializerMethodField()
    loan = serializers.SerializerMethodField()
    class Meta:
        model = Installments
        fields = "__all__"

    def get_amount_to_pay(self, obj):
        return obj.get_amount_to_pay
    
    def get_loan(self, obj):
        return obj.loan.business.name

        
class InstallmentCreateSerializer(serializers.ModelSerializer):
    'Installment Serializer that can be used by customer to create installments'
    class Meta:
        model = Installments
        fields = "__all__"
        read_only_fields = ("accepted_at" , "Loan" , "due_date" , "original_amount_due" , "paid")


            
        
            