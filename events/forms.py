from django import forms
from django.contrib.admin import widgets
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.utils.text import capfirst

# from Bootstrap import DatetimePicker
from .models import searchBandSugg, Document, band
from .models import Event


class bandForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label= ("Add bands to the search:"))
    class Meta:
        model= searchBandSugg
        fields= ["name"]


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label= ("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label= ("Password confirmation"),
        widget=forms.PasswordInput,
        help_text= ("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label= ("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login':  ("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive':  ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields= ['username', 'password']

class likeForm(forms.ModelForm):
    likes = forms.IntegerField()
    class Meta:
        # model = Event
        fields= ['likes']

class DocumentForm(forms.ModelForm):
    # date = forms.DateField(widget=widgets.AdminDateWidget, required=False)
    # document = forms.FileField(upload_to='documents/')
    # uploaded_at = forms.DateTimeField(auto_now_add=True)
    # band = forms.CharField(max_length=255, blank=True)
    # venue = forms.CharField(max_length=255, blank=True)
    class Meta:
        model = Document
        fields=["document",]

