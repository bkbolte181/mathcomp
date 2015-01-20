from django import forms
from competition.models import *
from django.conf import settings

class LoginForm(forms.Form):
	''' On log in, you only need an email and a password '''
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class SignupForm(forms.ModelForm):
	''' This is the main sign-up form '''
	error_messages = { # Add errors here
		'password_mismatch': 'The two password fields didn\'t match.',
        }
	# Form needs two passwords to make sure the user doesn't mistype
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text-center', 'placeholder': 'Password'}), label='Password', help_text='Choose a password')
	retype_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text-center', 'placeholder': 'Retype Password'}), label='Retype Password', help_text='Enter the same password as above, for verification.')

	class Meta:
		model = SiteUser
		
		# These are the fields that the user needs to input when they create their account
		fields = ('email', 'first_name', 'last_name')
		widgets = {
				'email': forms.EmailInput(attrs={'class': 'form-control text-center', 'placeholder': 'Email Address'}),
				'first_name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'First Name'}),
				'last_name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Last Name'}),
		    }

	# This method validates that the two passwords are the same
	# If they don't match it throws an error
	def clean_retype_password(self):
		password = self.cleaned_data.get('password')
		retype_password = self.cleaned_data.get('retype_password')
		if password and retype_password and password != retype_password:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			    )
		return retype_password

	# This is the method for saving the newly created user
	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

class GetPasswordReset(forms.ModelForm):
	class Meta:
		model = ResetPassword
		fields = ('email',)
		widgets = {
			'email': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Enter Email Address'}),
		}

class ResetPasswordForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text-center', 'placeholder': 'Password'}), label='Password', help_text='Choose a password')
	retype_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text-center', 'placeholder': 'Retype Password'}), label='Retype Password', help_text='Enter the same password as above, for verification.')
	
	def clean_retype_password(self):
		password = self.cleaned_data.get('password')
		retype_password = self.cleaned_data.get('retype_password')
		if password and retype_password and password != retype_password:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			    )
		return retype_password
	
	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

class UpdateForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ('title', 'message',)
		widgets = {
			'title': forms.TextInput(attrs={'placeholder': 'Title'}),
			'message': forms.Textarea(attrs={'placeholder': 'Message'}),
		}