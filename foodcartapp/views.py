import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@api_view(['POST'])
def register_order(request):
    try:
        order = json.loads(request.body.decode())
        product = order['products'][0]
        product_instance = Product.objects.get(id=product['product'])
        new_order = Order.objects.create(
            address=order['address'],
            name=order['firstname'],
            surname=order['lastname'],
            contact_phone=order['phonenumber'],
        )
        OrderElements.objects.create(
            order=new_order,
            product=product_instance,
            product_number=product['quantity'],
        )
    except ValueError:
        pass
    orders = Order.objects.all()
    registers_order = []
    for order in orders:
        register_order.append({
            'address': order.address,
            'name': order.name,
            'surname': order.surname,
            'contact_phone': str(order.contact_phone)
        })
    return Response(registers_order)
