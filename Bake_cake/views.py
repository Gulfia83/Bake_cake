from django.shortcuts import render, get_object_or_404, redirect
from tg_bot.models import LinkClick


def index(request):
    return render(request, "index.html")


def lk(request):
    return render(request, "lk.html")


def lk_order(request):
    return render(request, "lk-order.html")


def track_link(request, link_id):
    link = get_object_or_404(LinkClick, id=link_id)
    link.click_count += 1
    link.save()
    return redirect(link.url)
