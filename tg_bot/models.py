from django.db import models


class Level(models.Model):
    number = models.IntegerField(verbose_name="Число уровней")
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name_plural = 'Уровни'

    def __str__(self):
        if self.number == 1:
            return f"{self.number} уровень"
        else:
            return f"{self.number} уровня"


class Shape(models.Model):
    name = models.CharField(verbose_name="Форма", max_length=20)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name_plural = 'Форма'

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(verbose_name="Топпинг", max_length=50)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.name


class Berries(models.Model):
    name = models.CharField(verbose_name="Ягоды", max_length=50)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.name


class Decor(models.Model):
    name = models.CharField(verbose_name="Декор", max_length=50)
    price = models.FloatField(verbose_name="Цена", default=0.0)

    class Meta:
        verbose_name_plural = 'Декор'

    def __str__(self):
        return self.name


class Catalog(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название торта", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    price = models.FloatField(verbose_name="Цена", blank=True, null=True)
    image = models.ImageField(upload_to="cakes", verbose_name="Изображение торта", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Каталог'

    def __str__(self):
        return self.title


class Cake(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    level = models.OneToOneField(Level, on_delete=models.SET_NULL, null=True)
    shape = models.OneToOneField(Shape, on_delete=models.SET_NULL, null=True)
    topping = models.OneToOneField(Topping, on_delete=models.SET_NULL, null=True)
    berries = models.OneToOneField(Berries, on_delete=models.SET_NULL, null=True, blank=True)
    decor = models.OneToOneField(Decor, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(verbose_name="Надпись на торте", max_length=200, null=True, blank=True)
    price = models.FloatField(default=0.0, verbose_name="Цена")

    class Meta:
        verbose_name_plural = 'Торты'

    def __str__(self):
        return self.title


class LinkClick(models.Model):
    url = models.URLField(max_length=200, null=True)  # Тут будет ссылка на телеграмм бота
    click_count = models.PositiveIntegerField(default=0, null=True)
    last_clicked = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.url


class Client(models.Model):
    name = models.CharField('ФИО', max_length=200)
    email = models.EmailField('email', unique=True)
    phone = models.CharField('Телефон', max_length=200)
    telegram_id = models.CharField('телеграмм ID', max_length=50)
    address = models.TextField('адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    client = models.ForeignKey(Client,
                               verbose_name='клиент',
                               on_delete=models.CASCADE,
                               related_name='orders')
    date = models.DateField(auto_now_add=True)
    address = models.TextField('адрес')
    # box = models.OneToOneField(Box, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField('цена', null=True, blank=True)

    def __str__(self):
        return f'заказ {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'