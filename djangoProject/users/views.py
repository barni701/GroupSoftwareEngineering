from django.shortcuts import render, redirect


from django.contrib.auth.forms import UserCreationForm
# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup_new.html', {'form': form})


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