# Generated by Django 4.1.5 on 2024-08-20 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkClick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(null=True)),
                ('click_count', models.PositiveIntegerField(default=0, null=True)),
                ('last_clicked', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cake',
            name='berries',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.berries'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='decor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg_bot.decor'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='text',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Надпись на торте'),
        ),
    ]