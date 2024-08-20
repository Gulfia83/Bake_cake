from django.contrib import admin
from .models import Cake, CustomizationCategory, CustomizationOption, CustomizationChoice, Order


class CustomizationOptionInline(admin.TabularInline):
    model = CustomizationOption
    extra = 1


class CustomizationCategoryAdmin(admin.ModelAdmin):
    inlines = [CustomizationOptionInline]


class CustomizationChoiceInline(admin.TabularInline):
    model = CustomizationChoice
    extra = 1


class CustomizationOptionAdmin(admin.ModelAdmin):
    inlines = [CustomizationChoiceInline]


class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'delivery')
    search_fields = ('name', 'description')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_cake', 'status', 'total_price')
    search_fields = ('id', 'user__name')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')

    def get_cake(self, obj):
        if obj.cake:
            return obj.cake.name
        elif obj.customizations.exists():
            return 'Кастомизированный торт'
        else:
            return 'Не выбран'

    get_cake.short_description = 'Торт'


admin.site.register(Cake, CakeAdmin)
admin.site.register(CustomizationCategory, CustomizationCategoryAdmin)
admin.site.register(CustomizationOption, CustomizationOptionAdmin)
admin.site.register(Order, OrderAdmin)
