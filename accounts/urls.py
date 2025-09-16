from django.urls import path
from .views import RegisterView, LoginView, LogoutView, profile, ActivateAccountView, AccountSettings

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:id>/', profile, name='profile'),
    path('accounts/activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('account/settings/', AccountSettings.as_view(), name='settings'),

]
