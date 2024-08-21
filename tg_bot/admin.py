from django.contrib import admin
from tg_bot.models import Level, Shape, Topping, Berries, Decor, Cake
from tg_bot.models import LinkClick, Client, Order


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["telegram_id", "name"]
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "created_at"]


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["number", "price"]

@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ["title", "level", "shape", "topping", "berries", "decor"]


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "click_count",
        "last_clicked",
    )
