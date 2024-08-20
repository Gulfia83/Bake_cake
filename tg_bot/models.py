from django.db import models


class Level(models.Model):
    number = models.IntegerField(verbose_name='Число уровней')
    price = models.FloatField(verbose_name='Цена',
                              default=0.0)

    def __str__(self):
        return f'{self.number} уровня'


class Shape(models.Model):
    name = models.CharField(verbose_name='Форма',
                            max_length=20)
    price = models.FloatField(verbose_name='Цена',
                              default=0.0)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(verbose_name='Топпинг',
                            max_length=50)
    price = models.FloatField(verbose_name='Цена',
                              default=0.0)

    def __str__(self):
        return self.name


class Berries(models.Model):
    name = models.CharField(verbose_name='Ягоды',
                            max_length=50)
    price = models.FloatField(verbose_name='Цена',
                              default=0.0)

    def __str__(self):
        return self.name


class Decor(models.Model):
    name = models.CharField(verbose_name='Декор',
                            max_length=50)
    price = models.FloatField(verbose_name='Цена',
                              default=0.0)
    
    def __str__(self):
        return self.name


class Catalog(models.Model):
    title = models.CharField(max_length=50,
                             verbose_name='Название торта')
    description = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    image = models.ImageField(upload_to='cakes',
                              verbose_name='Изображение торта')

    def __str__(self):
        return self.title


class Cake(models.Model):
    title = models.CharField(max_length=50,
                             verbose_name='Название')
    level = models.OneToOneField(Level,
                                 on_delete=models.SET_NULL,
                                 null=True)
    shape = models.OneToOneField(Shape, 
                                 on_delete=models.SET_NULL,
                                 null=True)
    topping = models.OneToOneField(Topping,
                                   on_delete=models.SET_NULL,
                                   null=True)
    berries = models.OneToOneField(Berries,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    decor = models.OneToOneField(Decor,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    text = models.TextField(verbose_name='Надпись на торте',
                            max_length=200,
                            null=True,
                            blank=True)
    price = models.FloatField(default=0.0,
                              verbose_name='Цена')

    def __str__(self):
        return self.title
