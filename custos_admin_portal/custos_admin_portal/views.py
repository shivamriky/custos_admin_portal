from django.shortcuts import render


def home(request):
    return render(request, 'custos_admin_portal/home.html', {})

