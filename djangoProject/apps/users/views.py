from decimal import Decimal, InvalidOperation
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging
from .forms import ProfileUpdateForm, TCConsentForm, CustomSignUpForm
from .models import UserProfile


from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required
def delete_account(request):
    user = request.user
    logout(request)  # Logs the user out
    user.delete()  # Deletes the user account
    messages.success(request, "Your account has been deleted successfully.")
    return redirect('landing')  # Redirect after deletion

def logout_user(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Initialize UserProfile with default currency balance
            UserProfile.objects.create(user=user, tc_consent=form.cleaned_data['tc_consent'], currency_balance=Decimal('100.00'))  # Starting balance
            login(request, user)
            return redirect('users:landing')
    else:
        form = CustomSignUpForm()
    return render(request, 'users/signup_new.html', {'form': form})

def landing(request):
    return render(request, 'users/landing.html')


def terms_and_conditions(request):
    return render(request, 'users/tc.html')

def privacy_policy(request):
    return render(request, 'users/privacy_policy.html')

logger = logging.getLogger(__name__)

@login_required
def profile_view(request):
    """Handles profile updates including GDPR consent and currency balance display."""
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=user)
        tc_form = TCConsentForm(request.POST, instance=user_profile)

        if profile_form.is_valid() and tc_form.is_valid():
            profile_form.save()
            tc_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=user)
        tc_form = TCConsentForm(instance=user_profile)

    return render(request, 'users/profile.html', {
        'profile_form': profile_form,
        'tc_form': tc_form,
        'currency_balance': user_profile.currency_balance  # Send balance to template
    })

@login_required
def user_data_view(request):
    """GDPR-compliant view to show and export user data."""
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    user_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "tc_consent": user_profile.tc_consent,
    }

    # Export data as JSON
    if request.GET.get("export") == "json":
        return JsonResponse(user_data, safe=False)

    return render(request, "users/user_data.html", {"user_data": user_data})

@login_required
def add_currency(request):
    if request.method == "POST":
        amount = request.POST.get("amount", None)
        if amount is None:
            return JsonResponse({'error': 'Amount is required.'}, status=400)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return JsonResponse({'error': 'Invalid amount provided.'}, status=400)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.add_currency(amount, description="User added funds")
        return JsonResponse({'new_balance': str(user_profile.currency_balance)})
    return JsonResponse({'error': 'POST method required.'}, status=405)

@login_required
def spend_currency(request):
    if request.method == "POST":
        amount = request.POST.get("amount", None)
        if amount is None:
            return JsonResponse({'error': 'Amount is required.'}, status=400)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return JsonResponse({'error': 'Invalid amount provided.'}, status=400)
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.deduct_currency(amount, description="User spent funds"):
            return JsonResponse({'new_balance': str(user_profile.currency_balance)})
        return JsonResponse({'error': 'Insufficient balance.'}, status=400)
    return JsonResponse({'error': 'POST method required.'}, status=405)

@login_required
def transaction_history(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = user_profile.transactions.all().order_by("-created_at")
    return render(request, "users/transaction_history.html", {"transactions": transactions})