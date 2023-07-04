from rest_framework import serializers

def is_positive (value):
    'validate that the value is positive'
    if value <1 :
        raise serializers.ValidationError('Not an allowed value')

def is_positive_or_zero (value):
    'validate that the value is positive or zero'
    if value <0 :
        raise serializers.ValidationError('Not an allowed value')
    
def is_negative1_or_positive (value):
    'validate that the value is positive or -1'
    if value < -1:
        raise serializers.ValidationError('Not an allowed value')

def allowed_months(value):
    'validate that the value is greater than 1 and less than 60'
    if value < 2 or value > 60:
        raise serializers.ValidationError('Not an allowed value')


