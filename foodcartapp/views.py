from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.validators import validate_international_phonenumber
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

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
        order = request.data
        if 'products' in order:
            product = order['products']
        else:
            return Response({'error': 'Product key not presented or not list'})
        if not isinstance(product, list) or product == []:
            return Response({'error': 'Product key not presented or not list'})
        if 'address' not in order or 'firstname' not in order or 'lastname' not in order:
            return Response({'error': 'Order key not presented or not list'})

        product = order['products'][0]
        if 'product' not in product or 'quantity' not in product:
            return Response({'error': 'Product key not presented or not list'})

        product_instance = Product.objects.filter(id=product['product']).first()
        if not product_instance:
            return Response({'error': 'Invalid product ID'})

        if not order['firstname']:
            return Response({'error': 'Firstname field cannot be empty'})
        if not order['lastname']:
            return Response({'error': 'Lastname field cannot be empty'})
        if not order['phonenumber']:
            return Response({'error': 'Phonenumber field cannot be empty'})
        if not order['address']:
            return Response({'error': 'Address field cannot be empty'})
        try:
            phone_number = PhoneNumber.from_string(order['phonenumber'])
            validate_international_phonenumber(phone_number)
        except ValidationError:
            return Response({'error': 'Invalid phone number'})

        new_order = Order.objects.create(
            address=order['address'],
            name=order['firstname'],
            surname=order['lastname'],
            contact_phone=phone_number,
        )
        OrderElements.objects.create(
            order=new_order,
            product=product_instance,
            product_number=product['quantity'],
        )

    except ValueError as e:
        return Response({'error': str(e)})

    orders = Order.objects.all()
    registers_order = []
    for order in orders:
        registers_order.append({
            'address': order.address,
            'name': order.name,
            'surname': order.surname,
            'contact_phone': str(order.contact_phone)
        })
    print(registers_order)
    return Response()
