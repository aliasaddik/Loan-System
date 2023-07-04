from rest_framework import serializers
from Loan.myapp.models.customers import Customer
class CustomerSerializer(serializers.ModelSerializer):
    id_front = serializers.SerializerMethodField()
    id_back = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "date_of_birth",
            "id_front",
            "id_back",
            "current_debt_outside", 
            "credit_limit_outside",  
            "credit_history_length",
            "pursuit_of_new_credit",
            "months_since_last_late_payment", 
            "credit_mix",
            "created_at" 
        )

    def get_id_front(self, obj):
            return obj.id_front.url if obj.id_front else None
    def get_id_back(self, obj):
            return obj.id_back.url if obj.id_back else None
        
class CustomerGetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True, required = False)

    class Meta:
        model = Customer
        fields = ("email","id","full_name")
 