from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SettingsForm
from .models import Profile
from posts.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
token_generator = PasswordResetTokenGenerator()


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('posts:home_feed')
        return render(request, 'accounts/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('posts:home_feed')

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                try:
                    user_exist = User.objects.get(username=username)
                    if not user_exist.is_active:
                        messages.error(request, 'Please verify your email before logging in.')
                    else:
                        messages.error(request, 'Invalid credentials, try again')
                except User.DoesNotExist:
                    messages.error(request, 'Invalid credentials, try again')
                return render(request, 'accounts/login.html')

            login(request, user)
            messages.success(request, f'Welcome, {user.username}! You are now logged in.')
            return redirect('posts:home_feed')

        else:
            messages.error(request, 'Please fill all fields')
        return render(request, 'accounts/login.html')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('posts:home_feed')
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send Activation Email
            current_site = get_current_site(request)
            subject = "Activate Your SocialHub Account"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"

            # Render the HTML email template
            html_message = render_to_string('accounts/send_email.html', {
                'user': user,
                'activation_link': activation_link
            })

            # Send email
            send_mail(
                subject,
                f"Hi {user.username}, please use this link to activate your account: {activation_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=html_message  # THIS is needed for HTML
            )

            messages.success(request, 'Account created successfully! Please check your email to activate your account.')
            return redirect('accounts:register')
        else:
            if form.errors:
                first_error = list(form.errors.items())[0]
                field, error = first_error
                field = field.replace('_', ' ').capitalize()
                messages.error(request, error[0].replace('This field', field))
            else:
                messages.error(request, 'An error occurred during registration')
            return redirect('accounts:register')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            user = None

        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated! You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'The activation link is invalid or has expired.')
            return redirect('accounts:register')


@login_required
def profile(request, id=None):

    profile_user = get_object_or_404(User, id=id) if id else request.user
    allowed_privacy = ['public']
    if profile_user.profile.is_visible or profile_user == request.user:
        if profile_user == request.user:
            posts = Post.objects.filter(Q(author=profile_user)).order_by('-created_at')
        else:
            posts = Post.objects.filter(Q(author=profile_user) and Q(privacy__in=allowed_privacy)).order_by('-created_at')

        if request.method == 'POST' and profile_user == request.user:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            if u_form.is_valid() and p_form.is_valid():
                user = u_form.save(commit=False)
                user.save()
                p_form.save()

                # 🔑 Keep session alive after updating User
                update_session_auth_hash(request, user)

                messages.success(request, '✅ Your profile has been updated!')
                return redirect('accounts:profile', id=request.user.id)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        messages.error(request, 'This account is private')
        return redirect("posts:home_feed")
    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile_user': profile_user,
        'posts': posts,
    })


@method_decorator(login_required, name="dispatch")
class AccountSettings(View):
    template_name = "accounts/settings.html"

    def get(self, request):
        form = SettingsForm(instance=request.user.profile)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SettingsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your settings have been updated ✅")
            return redirect("accounts:settings")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('accounts:login')
