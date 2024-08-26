# Generated by Django 4.1.5 on 2024-08-26 01:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0002_linkclick_alter_cake_berries_alter_cake_decor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=50, unique=True, verbose_name='Телеграм ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='RU', verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='Адрес доставки')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания заказа')),
                ('production_time', models.IntegerField(default=3, verbose_name='Срок исполнения заказа')),
                ('price', models.FloatField(default=0.0, verbose_name='Цена')),
                ('comments', models.TextField(blank=True, max_length=200, null=True, verbose_name='Комментарии')),
                ('status', models.CharField(choices=[('under', 'на рассмотрении'), ('todo', 'принят в работу'), ('true', 'подтвержден'), ('topay', 'выставить счет'), ('false', 'отменен'), ('delay', 'задерживается')], default='under', max_length=30, verbose_name='Статус заказа')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.DeleteModel(
            name='Catalog',
        ),
        migrations.AlterModelOptions(
            name='berries',
            options={'verbose_name_plural': 'Ягоды'},
        ),
        migrations.AlterModelOptions(
            name='cake',
            options={'verbose_name': 'Торт', 'verbose_name_plural': 'Торты'},
        ),
        migrations.AlterModelOptions(
            name='decor',
            options={'verbose_name': 'Декор', 'verbose_name_plural': 'Декор'},
        ),
        migrations.AlterModelOptions(
            name='level',
            options={'verbose_name': 'Уровень', 'verbose_name_plural': 'Уровни'},
        ),
        migrations.AlterModelOptions(
            name='shape',
            options={'verbose_name': 'Форма', 'verbose_name_plural': 'Форма'},
        ),
        migrations.AlterModelOptions(
            name='topping',
            options={'verbose_name': 'Топпинг', 'verbose_name_plural': 'Топпинги'},
        ),
        migrations.RemoveField(
            model_name='cake',
            name='price',
        ),
        migrations.AddField(
            model_name='cake',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание торта'),
        ),
        migrations.AddField(
            model_name='cake',
            name='end_price',
            field=models.FloatField(default=0.0, verbose_name='Итоговая цена'),
        ),
        migrations.AddField(
            model_name='cake',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cakes', verbose_name='Изображение торта'),
        ),
        migrations.AddField(
            model_name='cake',
            name='ready_to_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cake',
            name='berries',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.berries'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='decor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.decor'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.level'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='shape',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.shape'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='topping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.topping'),
        ),
        migrations.AddField(
            model_name='order',
            name='cake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tg_bot.cake', verbose_name='Заказанный торт'),
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='tg_bot.client', verbose_name='Клиент'),
        ),
    ]
