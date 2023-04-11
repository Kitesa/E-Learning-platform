from .models import Account
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AccountCreationForm(UserCreationForm):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Other'),
        )
    email 				= forms.EmailField(max_length = 70)
    username 			= forms.CharField(max_length = 30)
    first_name			= forms.CharField(max_length = 30)
    Phone_Number 		= forms.CharField(max_length=12)
    birth_date          = forms.DateTimeField()
    gender              = forms.ChoiceField(choices=gender_choices)
    
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'Phone_Number', 'email', 'gender', 'birth_date', 'password1', 'password2')


    def clean_Phone_Number(self):
        Phone_Number = self.cleaned_data['Phone_Number']

        if Phone_Number[:4] != "+251":
                raise forms.ValidationError("Invalid phone number country code!(+251)")
        else:
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(Phone_Number=Phone_Number)
            except Account.DoesNotExist:
                return Phone_Number
            raise forms.ValidationError('Phone Number "%s" is already in use.' % Phone_Number)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
