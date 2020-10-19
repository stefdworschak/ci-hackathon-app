from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import USER_TYPE_CHOICES, LMS_MODULES_CHOICES


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    slack_display_name = forms.CharField(max_length=30, label='Slack display name')
    user_type = forms.CharField(widget=forms.Select(
                               choices=USER_TYPE_CHOICES))
    current_lms_module = forms.CharField(widget=forms.Select(
                               choices=LMS_MODULES_CHOICES))

    class Meta:
        fields = ('email','password1','password2',
                  'slack_display_name', 'user_type', 'current_lms_module')
        model = get_user_model()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']
        user.slack_display_name = self.cleaned_data['slack_display_name']
        user.user_type = self.cleaned_data['user_type']
        user.current_lms_module = self.cleaned_data['current_lms_module']
        if self.cleaned_data['user_type'] == 'participant':
            user.is_active = True
        elif self.cleaned_data['user_type'] == 'admin':
            user.is_staff = True
            user.is_active = False
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = False
        user.save()