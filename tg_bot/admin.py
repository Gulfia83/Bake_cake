from django.contrib import admin
from tg_bot.models import Level, Shape, Topping, Berries, Decor, Catalog, Cake, LinkClick, Client

admin.site.register(Level)
admin.site.register(Shape)
admin.site.register(Topping)
admin.site.register(Berries)
admin.site.register(Decor)
admin.site.register(Catalog)
admin.site.register(Cake)
admin.site.register(Client)


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "click_count",
        "last_clicked",
    )
