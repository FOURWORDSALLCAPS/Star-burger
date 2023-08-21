from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Order, OrderElements


class OrderElementsSerializer(ModelSerializer):
    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


def validate_products(value):
    if value:
        return value
    raise ValidationError('Expects products field to be a non-empty list')


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber', 'products']
