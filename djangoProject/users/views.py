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
        form = UserCreationForm()

    return render(request, 'users/templates/registration/signup.html', {'form': form})
