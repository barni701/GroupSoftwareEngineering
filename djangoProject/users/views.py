from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from .forms import SignUpForm, ProfileUpdateForm, GDPRConsentForm
from .models import UserProfile


from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required
def delete_account(request):
    user = request.user
    user.delete()  # Deletes the user account
    return redirect('landing')  # Redirect after deletion

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save GDPR consent
            UserProfile.objects.create(user=user, gdpr_consent=form.cleaned_data['gdpr_consent'])
            login(request, user)  # Log the user in after signup
            return redirect('landing')  # Redirect to the landing page or another page
    else:
        form = SignUpForm()
    return render(request, 'users/signup_new.html', {'form': form})


def landing(request):
    return render(request, 'users/landing.html')


def privacy_policy(request):
    return render(request, 'users/tc.html')

logger = logging.getLogger(__name__)

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        new_email = request.POST.get('email')

        logger.info(f"User {user.username} changed email to {new_email}")  # Logs changes

        user.email = new_email
        user.save()

    return render(request, 'users/profile.html')


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