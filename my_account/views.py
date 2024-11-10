from django.shortcuts import render
from .models import Purchase
from django.contrib.auth.decorators import login_required

@login_required
def my_account(request):
    purchases = Purchase.objects.filter(user=request.user, payment_verified=True)
    return render(request, 'my_account/my_account.html', {'purchases': purchases})
