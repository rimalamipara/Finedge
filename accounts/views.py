from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout

def register(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data["username"] = post_data.get("username", "").lower()
        form = UserCreationForm(post_data)
        if form.is_valid():
            form.save()
            return redirect("accounts:signin")
    else:
        form = UserCreationForm()
    return render(request, "accounts/create_account.html", {"form": form})

def sign_in(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data["username"] = post_data.get("username", "").lower()
        form = AuthenticationForm(data=post_data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profiles:account_status")
        else:
            # This will run when form is invalid (wrong credentials)
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, "accounts/sign_in.html", {"form": form})

def logout_view(request):
    # Logout the user if he hits the logout submit button
    logout(request)
    return redirect("accounts:signin")
