from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Level(models.Model):
    number = models.IntegerField(verbose_name="Число уровней")
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"

    def __str__(self):
        if self.number == 1:
            return f"{self.number} уровень"
        else:
            return f"{self.number} уровня"


class Shape(models.Model):
    name = models.CharField(verbose_name="Форма", max_length=20)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Форма"

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(verbose_name="Топпинг", max_length=50)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинги"

    def __str__(self):
        return self.name


class Berries(models.Model):
    name = models.CharField(verbose_name="Ягоды", max_length=50)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name_plural = "Ягода"
        verbose_name_plural = "Ягоды"

    def __str__(self):
        return self.name


class Decor(models.Model):
    name = models.CharField(verbose_name="Декор", max_length=50)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name = "Декор"
        verbose_name_plural = "Декор"

    def __str__(self):
        return self.name


class Cake(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    level = models.OneToOneField(Level, on_delete=models.SET_NULL, null=True)
    shape = models.OneToOneField(Shape, on_delete=models.SET_NULL, null=True)
    topping = models.OneToOneField(Topping, on_delete=models.SET_NULL, null=True)
    berries = models.OneToOneField(Berries, on_delete=models.SET_NULL, null=True, blank=True)
    decor = models.OneToOneField(Decor, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(verbose_name="Надпись на торте", max_length=200, null=True, blank=True)
    end_price = models.FloatField(default=0.0, verbose_name="Итоговая цена")
    image = models.ImageField(upload_to="cakes", verbose_name="Изображение торта", null=True, blank=True)
    ready_to_order = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"

    def __str__(self):
        return self.title


class Client(models.Model):
    telegram_id = models.CharField(max_length=50, unique=True, verbose_name="Телеграм ID")
    name = models.CharField(max_length=200, verbose_name="ФИО")
    phonenumber = PhoneNumberField(region="RU", blank=True, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"

    def __str__(self):
        if self.username:
            return f'@{self.name}'
        else:
            return f'{self.telegram_id}'


class Order(models.Model):
    cake = models.ForeignKey(Cake, verbose_name="Заказанный торт", on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name="Заказчик", on_delete=models.CASCADE, related_name="orders")
    address = models.TextField(verbose_name="Адрес доставки")
    created_at = models.DateTimeField(verbose_name="Дата создания заказа", auto_now_add=True)
    delivery_time = models.IntegerField(verbose_name="Срок испольнения заказа", default=3)
    price = models.FloatField(verbose_name="Цена", default=0.0)
    comments = models.TextField(max_length=200, verbose_name="Комментарии")
    status = models.TextField(max_length=30, verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order #{self.number}"


class LinkClick(models.Model):
    url = models.URLField(max_length=200, null=True)  # Тут будет ссылка на телеграмм бота
    click_count = models.PositiveIntegerField(default=0, null=True)
    last_clicked = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.url
