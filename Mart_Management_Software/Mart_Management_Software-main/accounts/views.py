from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import CustomerProfile


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            phone = form.cleaned_data.get('phone', '')
            CustomerProfile.objects.create(user=user, phone=phone)
            login(request, user)
            messages.success(request, f'Welcome to Nepal Mart, {user.first_name}! Your account has been created.')
            return redirect('products:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_short_name() or form.get_user().username}!')
        return super().form_valid(form)


def logout_view(request):
    """Logout the user."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('products:home')


@login_required
def profile(request):
    """User profile view."""
    # Ensure profile exists
    profile_obj, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile_obj)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile.html', context)
