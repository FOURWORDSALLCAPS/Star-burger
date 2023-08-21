from rest_framework.serializers import ModelSerializer

from .models import Order, OrderElements


class OrderElementsSerializer(ModelSerializer):
    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber', 'products']
