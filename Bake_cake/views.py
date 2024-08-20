from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def lk(request):
    return render(request, 'lk.html')


def lk_order(request):
    return render(request, 'lk-order.html')