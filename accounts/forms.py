from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Leave blank if you do not want to change the password.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class SettingsForm(forms.ModelForm):
    VISIBILITY_CHOICES = [
        (True, "Visible to All"),
        (False, "Private"),
    ]

    is_visible = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Profile Visibility",
    )

    class Meta:
        model = Profile
        fields = [
            "privacy",
            "is_visible",
            "notify_on_like",
            "notify_on_comment",
        ]
        labels = {
            "privacy": "Default Post Privacy",
            "notify_on_like": "Receive notifications when someone likes your post",
            "notify_on_comment": "Receive notifications when someone comments on your post",
        }
        widgets = {
            "privacy": forms.Select(attrs={"class": "form-select"}),
            "notify_on_like": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "notify_on_comment": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_is_visible(self):
        """Convert the string value from the form back to boolean"""
        value = self.cleaned_data["is_visible"]
        return value == "True"
