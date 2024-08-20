from django.contrib import admin
from .models import LinkClick


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "click_count",
        "click_count",
    )
