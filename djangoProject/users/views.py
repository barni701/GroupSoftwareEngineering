from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging
from .forms import SignUpForm, ProfileUpdateForm, GDPRConsentForm, CustomSignUpForm
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

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save GDPR consent
            UserProfile.objects.create(user=user, gdpr_consent=form.cleaned_data['gdpr_consent'])
            login(request, user)  # Log the user in after signup
            return redirect('landing')  # Redirect to the landing page or another page
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


'''def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        new_email = request.POST.get('email')

        logger.info(f"User {user.username} changed email to {new_email}")  # Logs changes

        user.email = new_email
        user.save()

        return redirect('profile')  # This should trigger a redirect

    return render(request, 'users/profile.html', {'user': user})'''


@login_required
def profile_view(request):
    """Handles profile updates including GDPR consent."""
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=user)
        gdpr_form = GDPRConsentForm(request.POST, instance=user_profile)

        if profile_form.is_valid() and gdpr_form.is_valid():
            profile_form.save()
            gdpr_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=user)
        gdpr_form = GDPRConsentForm(instance=user_profile)

    return render(request, 'users/profile.html', {
        'profile_form': profile_form,
        'gdpr_form': gdpr_form
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
        "gdpr_consent": user_profile.gdpr_consent,
    }

    # Export data as JSON
    if request.GET.get("export") == "json":
        return JsonResponse(user_data, safe=False)

    return render(request, "users/user_data.html", {"user_data": user_data})