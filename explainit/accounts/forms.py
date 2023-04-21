from .models import (Account,
                        ProfilePic,
                        UserBio,
                        )
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AccountCreationForm(UserCreationForm):
    '''
    Form class for user registration
    '''
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
        '''
        take some cleaning on user phone number before registration
        '''
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
        '''
        clean user email before sending to database
        on registration
        '''
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')

    def clean_username(self):
        '''
        clean username before sending to database
        on registration
        '''
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use.')

class UserUpdateForm(forms.ModelForm):
    '''
    Model form for username update
    '''
    class Meta:
        model   = Account
        fields  = ['first_name', 'last_name','username']
        email   = forms.EmailField()

class ProfilePicUploadForm(forms.ModelForm):
    '''
    Model form for profile picture upload and update
    '''
    class Meta:
        model   = ProfilePic
        fields  = ["image", ]

class BioUpdateForm(forms.ModelForm):
    '''
    Model form for username update
    '''
    class Meta:
        model   = UserBio
        fields  = ['bio',]