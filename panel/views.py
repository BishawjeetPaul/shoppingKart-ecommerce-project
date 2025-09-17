from django.shortcuts import render
from account.models import CustomUser


# this function for admin-customization.
def admin_panel(request):
    return render(request, 'admin-panel.html')

