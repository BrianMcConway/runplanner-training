from django.shortcuts import render, redirect
from .models import Purchase
from products_v2.models import Product
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth import logout

@login_required
def my_account(request):
    """
    Landing Page / Dashboard:
    Provides an overview and quick links to profile and purchased plans.
    """
    purchases = Purchase.objects.filter(user=request.user, payment_verified=True)
    return render(request, 'my_account/my_account.html', {'purchases': purchases})

@login_required
def profile(request):
    """
    Profile Overview Page:
    Displays user's personal details.
    """
    return render(request, 'my_account/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    """
    Edit Profile Page:
    Allows users to update their personal information.
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('my_account:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'my_account/edit_profile.html', {'form': form})

@login_required
def purchased_plans(request):
    """
    Purchased Training Plans Page:
    Lists all training plans the user has purchased.
    """
    purchases = Purchase.objects.filter(user=request.user, payment_verified=True)
    return render(request, 'my_account/purchased_plans.html', {'purchases': purchases})

@login_required
def view_training_plan(request, id):
    """
    View Training Plan Details:
    Displays details of a specific training plan the user has purchased.
    """
    # Fetch the specific purchase to ensure the user has access
    purchase = get_object_or_404(Purchase, id=id, user=request.user, payment_verified=True)
    
    # Fetch the associated training plan (Product)
    training_plan = get_object_or_404(Product, id=purchase.training_plan.id)
    
    return render(request, 'my_account/view_training_plan.html', {'training_plan': training_plan})

@login_required
def delete_account(request):
    """
    Delete Account Page:
    Prompts the user to confirm account deletion and handles the deletion process.
    """
    if request.method == 'POST':
        # Delete the user's purchases first if needed
        Purchase.objects.filter(user=request.user).delete()
        
        # Delete the user account
        user = request.user
        logout(request)  # Log the user out before deletion
        user.delete()
        
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return render(request, 'my_account/delete_account.html')