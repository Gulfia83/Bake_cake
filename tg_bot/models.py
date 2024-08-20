from django.db import models


class Cake(models.Model):
    verbose_name = "Торт"
    verbose_name_plural = "Торты"
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='cakes', verbose_name="Изображение")
    delivery = models.IntegerField(default=3, verbose_name="Срок изготовления")
    is_custom = models.BooleanField(default=False, verbose_name='Кастомный торт')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'


class InscriptionField(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    max_length = models.IntegerField(default=255)


# Модель категории кастомизации
class CustomizationCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание категории')
    is_required = models.BooleanField(default=False, verbose_name='Обязательная категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория кастомизации'
        verbose_name_plural = 'Категории кастомизации'


# Модель опции кастомизации
class CustomizationOption(models.Model):
    category = models.ForeignKey(CustomizationCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена опции')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание опции')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = 'Опция кастомизации'
        verbose_name_plural = 'Опции кастомизации'


# Модель выбора кастомизации
class CustomizationChoice(models.Model):
    option = models.ForeignKey(CustomizationOption, on_delete=models.CASCADE, related_name='choices',
                               verbose_name='Опция')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='customizations', verbose_name='Заказ')

    def __str__(self):
        return f"{self.option.name} - {self.order.id}"

    class Meta:
        verbose_name = 'Выбор кастомизации'
        verbose_name_plural = 'Выборы кастомизации'


class User(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # ID пользователя из Telegram
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


# Модель заказа
class Order(models.Model):
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"
    STATUS_CHOICES = [
        ('created', 'Заказ сформирован'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('in_progress', 'Исполняется'),
        ('out_for_delivery', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ФИО")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказы")
    delivery_address = models.CharField(max_length=255, blank=True, null=True, default='', verbose_name="Адрес доставки")
    delivery_datetime = models.DateTimeField(verbose_name="Дата и время доставки")
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="Телефон")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Статус заказа")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    cake = models.ForeignKey(Cake, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Торт')
    custom_options = models.ManyToManyField(CustomizationOption, blank=True, verbose_name='Кастомные опции')

    def calculate_total_price(self):
        base_price = self.cake.price if self.cake else 0
        customization_price = sum(option.price for option in self.custom_options.all())
        return base_price + customization_price

    def save(self, *args, **kwargs):
        if not self.phone and self.user:
            self.phone = self.user.phone
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.cake.name if self.cake else 'Custom Cake'}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
