from tg_bot.models import Level, Shape, Topping, Berries, Decor, Catalog, LinkClick

#! запуск через PowerShell команда - >>> exec(open("db_fast_data.py", encoding="utf-8").read())


Level.objects.create(number="1", price=400)
Level.objects.create(number="2", price=750)
Level.objects.create(number="3", price=1100)

Shape.objects.create(name="Квадрат", price=600)
Shape.objects.create(name="Круг", price=600)
Shape.objects.create(name="Прямоугольник", price=1000)

Topping.objects.create(name="Без топпинга", price=0)
Topping.objects.create(name="Белый соус", price=200)
Topping.objects.create(name="Карамельный сироп", price=180)
Topping.objects.create(name="Кленовый сироп", price=200)
Topping.objects.create(name="Клубничный сироп", price=300)
Topping.objects.create(name="Черничный сироп", price=350)
Topping.objects.create(name="Молочный шоколад", price=200)

Berries.objects.create(name="Ежевика", price=400)
Berries.objects.create(name="Малина", price=300)
Berries.objects.create(name="Голубика", price=450)
Berries.objects.create(name="Клубника", price=500)

Decor.objects.create(name="Фисташки", price=300)
Decor.objects.create(name="Безе", price=400)
Decor.objects.create(name="Фундук", price=350)
Decor.objects.create(name="Пекан", price=300)
Decor.objects.create(name="Маршмеллоу", price=200)
Decor.objects.create(name="Марципан", price=280)

Catalog.objects.create(
    title="Шоколадное безумие",
    description="Торт полностью состоящий из шоколада",
    price=3000,
    image="https://www.google.com",
)

Catalog.objects.create(
    title="Кремовый торт",
    description="Торт с нежной кремовой начинкой",
    price=2000,
    image="https://www.google.com",
)


LinkClick.objects.create(url="https://t.me/BakeCake_buter_bot", click_count=1)
