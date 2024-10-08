# Generated by Django 4.1.5 on 2024-08-23 21:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0007_remove_client_address_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_time',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 27, 0, 37, 32, 356329), verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='tg_bot.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 24, 0, 37, 32, 356329), verbose_name='Дата создания заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('under', 'на рассмотрении'), ('todo', 'принять в работу'), ('true', 'подтвержден'), ('topay', 'выставить счет'), ('false', 'отменен')], default='under', max_length=30, verbose_name='Статус заказа'),
        ),
    ]
