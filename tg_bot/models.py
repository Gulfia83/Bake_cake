from django.db import models


class Cake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cakes')
    delivery = models.IntegerField(default=3, verbose_name="Delivery time (days)")

    def __str__(self):
        return self.name


# Модель категории кастомизации
class CustomizationCategory(models.Model):
    name = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CustomizationOption(models.Model):
    category = models.ForeignKey(CustomizationCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# Модель выбора кастомизации
class CustomizationChoice(models.Model):
    option = models.ForeignKey(CustomizationOption, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(max_length=255)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (+{self.extra_price}р)"

# Модель кастомизации торта
class CakeCustomization(models.Model):
    options = models.ManyToManyField(CustomizationOption)

    def __str__(self):
        return "Кастомизация торта"


class User(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # ID пользователя из Telegram
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Модель заказа
class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Заказ сформирован'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('in_progress', 'Исполняется'),
        ('out_for_delivery', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True, default='')
    delivery_datetime = models.DateTimeField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    cake = models.ForeignKey(Cake, on_delete=models.SET_NULL, null=True, blank=True)
    customizations = models.ManyToManyField(CustomizationChoice, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    inscription = models.CharField(max_length=255, null=True, blank=True,
                                   help_text="Мы можем разместить на торте любую надпись, например: «С днем рождения!»")

    def calculate_total_price(self):
        base_price = self.cake.price if self.cake else 0
        customization_price = sum(choice.extra_price for choice in self.customizations.all())
        inscription_price = 500 if self.inscription else 0
        self.total_price = (base_price + customization_price + inscription_price) * self.quantity

    def save(self, *args, **kwargs):
        if not self.phone and self.user:
            self.phone = self.user.phone
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.cake.name if self.cake else 'Custom Cake'}"
