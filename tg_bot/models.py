from django.db import models


class LinkClick(models.Model):
    url = models.URLField(max_length=200)  # Тут будет ссылка на телеграмм бота
    click_count = models.PositiveIntegerField(default=0)
    last_clicked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
