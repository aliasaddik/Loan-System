import decimal
from io import BytesIO
import os
from rest_framework import serializers
from Loan.myapp.models.loans import MyLoan
from Loan.myapp.serializers.customers import CustomerGetSerializer
from Loan.myapp.services.customers import get_customer_by_email
from Loan.myapp.services.merchant import get_merchant_by_id
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from django.core.validators import EmailValidator
from Loan.myapp.validators.integers import allowed_months, is_positive

class LoanGetSerializer(serializers.ModelSerializer):
    'Loan Serializer that can be used by the merchant to apply for the loan for the user'
    requested_amount = serializers.IntegerField(validators= [is_positive], help_text = "requested amount is not allowed")
    no_of_months = serializers.IntegerField(validators= [allowed_months], help_text = "number of months is not allowed")
    offer_pdf = serializers.SerializerMethodField()
    customer =  CustomerGetSerializer(read_only=True, required = False)
    business = serializers.SerializerMethodField()
    
    class Meta:
        model = MyLoan
        fields = (
            "requested_amount",
            "customer",
            "no_of_months",
            "accepted_amount",
            "total_amount",
            "business",
            "customer",
            "offer_pdf",
            "accepted", "id" 
        )
        read_only_fields = ("accepted_amount","total_amount","business","customer","offer_pdf")
    
    def get_offer_pdf(self, obj):
        return obj.offer_pdf.url if obj.offer_pdf else None
    
    
    
    def get_business(self, obj):
        return obj.business.name if obj.business else None
    

class LoanSerializer(serializers.Serializer):
    requested_amount = serializers.IntegerField(validators= [is_positive], help_text = "requested amount is not allowed")
    no_of_months = serializers.IntegerField(validators= [allowed_months], help_text = "number of months is not allowed")
    customer =  serializers.EmailField(help_text="Customer email")
    class Meta:
        model = MyLoan
        fields = (
            "requested_amount",
            "customer",
            "no_of_months",
        )
        
    
    def create(self, validated_data):
        requested_amount = validated_data['requested_amount']
        email =  validated_data['customer'] 
        customer = get_customer_by_email(email)
        if customer == None:
            raise serializers.ValidationError("user does not exist")
        no_of_months = validated_data['no_of_months']
        user= self.context['request'].user
        merchant = get_merchant_by_id(user.id)
        business = merchant.business
        lowest_end = business.lending_starting_range
        highest_end = business.lending_end_range
        range_size = (highest_end - lowest_end) / 5   
        sector = []
    

        for i in range(5):
          start_value = lowest_end + (i * range_size)
          sector.append(start_value)
        # get the business's accepted amount for the customer based on their credit score
        credit_score = customer.get_user_credit_score
        if credit_score < 118:
            limit = sector[0]
        elif credit_score < 174:
            limit = sector[1]
        elif credit_score < 229:
            limit = sector[2]
        elif credit_score < 285:
            limit = sector[3]
        else:
            limit = sector[4]

        # the limit is the smallest value between the business's accepted amount and remaining balance from credit limit
        balance = customer.get_credit_limit - customer.get_current_outstanding_debt
        if balance < 0:
            raise serializers.ValidationError("The user have exceeded their credit limit")
        accepted_amount = min(limit, balance, requested_amount)

        # calculate amount after adding interest based on the number of months
        # the total amount is calculated by adding the interest rate to the debt
        # assuming  this formula M=P×( (r(1+r)^n)/( ((1+r)^n)-1) )
        # where M is the monthly payment, P is the accepted amount, r is the interest rate, and n is the number of months
        rate = business.base_interest_rate/100
        monthly_payment = decimal.Decimal(accepted_amount) *  ((rate *  (1 + rate) ** no_of_months) /(((1+rate) **no_of_months) - 1))
        total_amount = monthly_payment * no_of_months

        
        # create the offer pdf
        pdf_filename = f"{customer.full_name}_loan_offer.pdf"
        c = canvas.Canvas(pdf_filename)
        c.setFont("Helvetica", 12)
        c.drawString(50, 750, f"User Name: {customer.full_name}")
        c.drawString(50, 720, f"Company Name: {business.name}")
        c.drawString(50, 690, f"Requested Amount: {requested_amount}")
        c.drawString(50, 660, f"Accepted Amount: {accepted_amount}")
        c.drawString(50, 630, f"Number of Months: {no_of_months}")
        c.drawString(50, 600, f"Interest Rate: {business.base_interest_rate} %")
        c.save()

        # Store the PDF in validated_data
        pdf_bytes = BytesIO()
        with open(pdf_filename, 'rb') as f:
            pdf_bytes = BytesIO(f.read())

        validated_data['offer_pdf'] = ContentFile(pdf_bytes.getvalue(), name=pdf_filename)

        # Clean up the temporary PDF file
        os.remove(pdf_filename)
        validated_data["interest_rate"] = business.base_interest_rate
        validated_data['accepted_amount'] = accepted_amount
        validated_data['total_amount'] = total_amount
        validated_data['business'] = business
        validated_data['customer'] = customer

        loan = MyLoan.objects.create( requested_amount= requested_amount, customer = customer, no_of_months = no_of_months,
                                     accepted_amount = accepted_amount, total_amount = total_amount, business = business, interest_rate = rate, offer_pdf = validated_data['offer_pdf'])
        
        return loan
        
class LoanStatsSerializer(serializers.Serializer):
    no_of_loans = serializers.IntegerField()
    total_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
         
