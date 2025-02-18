from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging
from .forms import SignUpForm
from .models import UserProfile


from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required
def delete_account(request):
    user = request.user
    user.delete()  # Deletes the user account
    return redirect('home')  # Redirect after deletion

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
    return render(request, 'users/signup.html', {'form': form})


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

    return render(request, 'profile.html')