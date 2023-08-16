from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError, ModelSerializer

from .models import Product, Order, OrderElements


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class OrderElementsSerializer(ModelSerializer):
    class Meta:
        model = OrderElements
        fields = ['product', 'product_number']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['address', 'name', 'surname', 'contact_phone', 'products']


@api_view(['POST'])
def register_order(request):
    try:
        order = request.data
        if not order['products']:
            raise ValidationError('Expects products field be a list')
        serializer = OrderSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['products'][0]
        new_order = Order.objects.create(
            address=serializer.validated_data['address'],
            name=serializer.validated_data['name'],
            surname=serializer.validated_data['surname'],
            contact_phone=serializer.validated_data['contact_phone'],
        )
        OrderElements.objects.create(
            order=new_order,
            product=product['product'],
            product_number=product['product_number'],
        )
        order = {
            'id': new_order.id,
            'address': new_order.address,
            'name': new_order.name,
            'surname': new_order.surname,
            'contact_phone': str(new_order.contact_phone),
        }
        return Response(order)
    except ValueError as e:
        return Response({'error': str(e)})
