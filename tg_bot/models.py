from django.db import models


class Cake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cakes')

    def __str__(self):
        return self.name


class Customization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='customizations')

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    customizations = models.ManyToManyField(Customization, blank=True)
    comment = models.TextField(blank=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_datetime = models.DateTimeField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_price(self):
        total_price = self.cake.price
        for customization in self.customizations.all():
            total_price += customization.price
        return total_price

    def __str__(self):
        return (f"Заказ #{self.id} от пользователя {self.user.name} - "
                f"{self.cake.name} ({', '.join([c.name for c in self.customizations.all()]) if self.customizations.exists() else 'без кастомизаций'}),"
                f"Статус: {self.get_status_display()}, "
                f"Цена: {self.calculate_price()} руб., "
                f"Дата и время доставки: {self.delivery_datetime}")
