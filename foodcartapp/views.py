from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.db import transaction
from foodcartapp.serializers import OrderSerializer, OrderElementsSerializer

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


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products = serializer.validated_data.pop('products')
        new_order = serializer.create(serializer.validated_data)

        for product in products:
            product_obj = product['product']
            OrderElements.objects.create(
                order=new_order,
                product=product_obj,
                quantity=product['quantity'],
                price=product_obj.price
            )
        order = {
            'id': new_order.id,
            'address': new_order.address,
            'firstname': new_order.firstname,
            'lastname': new_order.lastname,
            'phonenumber': str(new_order.phonenumber),
        }
        return Response(order)
    except ValueError as e:
        return Response({'error': str(e)})
