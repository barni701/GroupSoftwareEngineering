from decimal import Decimal, InvalidOperation
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging
from .forms import ProfileUpdateForm, TCConsentForm, CustomSignUpForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from apps.battlepass.models import UserBattlePass
from apps.users.models import UserProfile, FriendRequest


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
def dashboard(request):
    """Dashboard displaying user stats, transactions, achievements, and leaderboards."""
    user_profile = UserProfile.objects.select_related('user').get(user=request.user)
    user_battle_pass = UserBattlePass.objects.filter(user=request.user).select_related('battle_pass').first()

    # Fetch related transactions and achievements efficiently
    transactions = user_profile.transactions.all().order_by('-created_at')[:5]
    achievements = user_profile.achievements.all().order_by('-date_awarded')[:3]

    # Fetch leaderboard (top 10 users by level, then XP)
    leaderboard = UserProfile.objects.order_by('-level', '-experience_points')[:10]

    required_xp = user_profile.get_required_xp(user_profile.level)  # XP needed for the next level
    current_progress = user_profile.experience_points

    context = {
        'user_profile': user_profile,
        'user_battle_pass': user_battle_pass,
        'transactions': transactions,
        'achievements': achievements,
        'leaderboard': leaderboard,
        "required_xp": required_xp,
        "current_progress": current_progress,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def xp_status(request):
    user_profile = request.user.userprofile
    required_xp = user_profile.get_required_xp(user_profile.level)
    current_progress = user_profile.experience_points
    data = {
        "level": user_profile.level,
        "current_progress": current_progress,
        "required_xp": required_xp,
    }
    return JsonResponse(data)

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

@login_required
def friends_list(request):
    """Display the user's friends and incoming friend requests."""
    user_profile = request.user.userprofile
    friends = user_profile.friends.all()
    friend_requests = FriendRequest.objects.filter(to_user=user_profile)

    context = {
        'friends': friends,
        'friend_requests': friend_requests,
    }
    return render(request, "users/friends_list.html", context)

@login_required
def send_friend_request(request):
    """Send a friend request to another user by username."""
    if request.method == "POST":
        username = request.POST.get("username")
        to_user = UserProfile.objects.filter(user__username=username).first()

        if to_user and to_user != request.user.userprofile:
            if not FriendRequest.objects.filter(from_user=request.user.userprofile, to_user=to_user).exists():
                FriendRequest.objects.create(from_user=request.user.userprofile, to_user=to_user)
                messages.success(request, "Friend request sent!")
        else:
            messages.error(request, "User not found or invalid.")
    
    return redirect("users:friends_list")


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user.userprofile:
        friend_request.accept()
        messages.success(request, "Friend request accepted!")
    return redirect("users:friends_list")

@login_required
def remove_friend(request, user_id):
    """Remove a friend from the user's friend list."""
    user_profile = request.user.userprofile
    friend_profile = get_object_or_404(UserProfile, id=user_id)

    if user_profile.friends.filter(id=friend_profile.id).exists():
        user_profile.friends.remove(friend_profile)
        friend_profile.friends.remove(user_profile)  # Ensure it's removed both ways
        messages.success(request, "Friend removed successfully!")

    return redirect("users:friends_list")