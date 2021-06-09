from django.shortcuts import render
from django.http import HttpResponse


def index_view(request):
    context = {}
    return render(request, 'fishapp/index.html', context)


def base_view(request):
    context = {}
    return render(request, 'fishapp/base.html', context)
