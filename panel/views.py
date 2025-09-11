from django.shortcuts import render


def admin_panel(request):
    return render(request, 'panel/admin-panel.html')