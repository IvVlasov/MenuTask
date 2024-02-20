from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html')


def index_path(request, url_path):
    return render(request, 'app/index.html')
