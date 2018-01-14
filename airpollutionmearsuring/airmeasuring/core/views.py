from django.shortcuts import render


def error404(request):
    context = {}
    return render(request, 'page_404.html', context)


def error403(request):
    context = {}
    return render(request, 'page_403.html', context)


def error500(request):
    context = {}
    return render(request, 'page_500.html', context)


def error400(request):
    context = {}
    return render(request, 'page_400.html', context)

