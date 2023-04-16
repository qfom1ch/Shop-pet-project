# Generated by Django 4.1.7 on 2023-04-16 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_payment_id_alter_order_initiator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Создан'), (1, 'Оплачен'), (2, 'В пути'), (3, 'Доставлен'), (4, 'Отменен'), (5, 'Успешный возврат')], default=0, verbose_name='Статус'),
        ),
    ]
