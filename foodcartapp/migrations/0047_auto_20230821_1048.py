from django.db import migrations, models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def copy_order_elements(apps, schema_editor):
    OrderElements = apps.get_model('foodcartapp', 'OrderElements')
    NewOrderElements = apps.get_model('foodcartapp', 'NewOrderElements')

    for order_element in OrderElements.objects.all():
        new_order_element = NewOrderElements(
            order=order_element.order,
            product=order_element.product,
            quantity=order_element.quantity,
            price=order_element.price
        )
        new_order_element.save()


def validate_price(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s a negative number'),
            params={'value': value},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_alter_orderelements_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewOrderElements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity',
                 models.IntegerField(db_index=True, validators=[MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=2, max_digits=5,
                                              validators=[validate_price, MinValueValidator(0)])),
                ('order',
                 models.ForeignKey(on_delete=models.CASCADE, related_name='new_order_elements', to='foodcartapp.Order',
                                   verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=models.CASCADE, related_name='new_order_elements',
                                              to='foodcartapp.Product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'новый элемент заказа',
                'verbose_name_plural': 'новые элементы заказа',
            },
        ),
        migrations.RunPython(copy_order_elements),
    ]
