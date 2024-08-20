from django.contrib import admin
from .models import Cake, CustomizationCategory, CustomizationOption, CustomizationChoice, Order, User
from django import forms


class CustomizationOptionInline(admin.TabularInline):
    model = CustomizationOption
    extra = 1

class CustomizationCategoryAdmin(admin.ModelAdmin):
    inlines = [CustomizationOptionInline]
    list_display = ('name', 'description', 'is_required')
    search_fields = ('name', 'description')
    list_filter = ('is_required',)


class CustomizationOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)


class CustomizationChoiceInline(admin.TabularInline):
    model = CustomizationChoice
    extra = 0


class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'delivery', 'is_custom')
    search_fields = ('name', 'description')
    list_filter = ('is_custom',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_cake', 'status')
    inlines = [CustomizationChoiceInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.cake and obj.cake.is_custom:
            categories = CustomizationCategory.objects.all()
            form.base_fields['custom_categories'] = forms.ModelMultipleChoiceField(
                queryset=categories,
                widget=forms.SelectMultiple,
                required=False,
                label='Категории кастомизации'
            )
        return form

    search_fields = ('id', 'user__name')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')

    def get_cake(self, obj):
        if obj.cake:
            return obj.cake.name
        elif obj.custom_cake:
            return obj.custom_cake.name
        elif obj.customizations.exists():
            return 'Кастомизированный торт'
        else:
            return 'Не выбран'

    get_cake.short_description = 'Торт'


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')
    search_fields = ('name', 'phone')


admin.site.register(Cake, CakeAdmin)
admin.site.register(CustomizationCategory, CustomizationCategoryAdmin)
admin.site.register(CustomizationOption, CustomizationOptionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)
