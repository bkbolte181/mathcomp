from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from competition.forms import *

import random

def is_staff(user):
	return user.is_staff

def home(request):
	''' Home page '''
	context = {
		'current_page': 'home',
	}
	if request.user.is_authenticated():
		return render(request, 'competition_home.html', context)
	else:
		return render(request, 'competition_splash.html', context)

def newpassword(request):
	''' Set new password '''
	context = {}
	if request.POST:
		form = ResetPasswordForm(request.POST)
		if form.is_valid() and 'identifier' in request.POST:
			new_password = form.cleaned_data['password']
			reset_obj = ResetPassword.objects.get(identifier = request.POST['identifier'])
			users = SiteUser.objects.filter(email=reset_obj.email)
			if users.count():
				user = users.first()
				user.set_password(new_password)
				user.save()
				reset_obj.delete()
				return HttpResponseRedirect(reverse('competition:home'))
		context['message'] = 'Your password update failed.'
	elif 'id' in request.GET and ResetPassword.objects.filter(identifier=request.GET['id']).count():
		r = ResetPassword.objects.filter(identifier=request.GET['id'])
		form = ResetPasswordForm()
		context['id'] = request.GET['id']
		context['form'] = form
	else:
		context['message'] = 'Where did you get this url? You should go somewhere else.'
	return render(request, 'new_password.html', context)

def resetpassword(request):
	''' Reset your password '''
	context = {}
	if request.POST:
		form = GetPasswordReset(request.POST)
		if form.is_valid() and SiteUser.objects.filter(email=form.cleaned_data['email']).exists():
			random_hash = "%032x" % random.getrandbits(128) # Generate random hash for resetting password
			ResetPassword.objects.filter(email=form.cleaned_data['email']).delete() # Delete any old objects
			password_reset_object = ResetPassword.objects.create(email=form.cleaned_data['email'], identifier=random_hash) # Create new object
			password_reset_object.save()
			
			email_content = 'You have requested that your password be reset. The url to do this is '
			email_content = email_content + reverse('competition:newpassword') + '?id=' + random_hash
			
			email_address = str(form.cleaned_data['email'])
			
			''' Need to send the email address here '''
			
			context['message'] = 'Your password reset email has been sent.'
		else:
			context['message'] = 'Your email address was not found.'
	else:
		form = GetPasswordReset()
		context['message'] = 'Enter your email address to reset your password.'
	context['form'] = form
	return render(request, 'reset_password.html', context)

def info(request):
	''' Info '''
	context = {
		'current_page': 'info',
	}
	return render(request, 'competition_info.html', context)

@login_required
def updates(request):
	context = {
		'current_page': 'updates',
		'announcements': Announcement.objects.order_by('-created_at'),
	}
	return render(request, 'competition_updates.html', context)

@user_passes_test(is_staff)
def participants(request):
	context = {
		'current_page': 'participants',
	}
	context['all_competitors'] = SiteUser.objects.all()
	return render(request, 'competition_participants.html', context)

@user_passes_test(is_staff)
def createupdate(request):
	if request.POST:
		form = UpdateForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('competition:updates'))
	else:
		form = UpdateForm()
	context = {
		'current_page': 'createupdate',
		'form': form,
	}
	return render(request, 'competition_createupdate.html', context)

@login_required
def auth_delete(request):
	''' Delete an account '''
	context = {}
	user = SiteUser.objects.get(email=request.user.email)
	user.delete()
	return HttpResponseRedirect(reverse('competition:home'))

def signin(request):
	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				if request.GET.get('next', False):
					return HttpResponseRedirect(request.GET.get('next', False))
				else:
					return HttpResponseRedirect(reverse('competition:home'))
	else:
		form = LoginForm()
	context = {
		'pagetitle': 'Sign In',
		'title': 'Please sign in',
		'buttontext': 'Sign In',
		'form': form,
	}
	return render(request, 'login.html', context)

def createaccount(request):
	if request.POST:
		form = SignupForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.clean_retype_password()
			form.save()
			user = authenticate(email=email, password=password)
			login(request, user)
			return HttpResponseRedirect(reverse('competition:home'))
	else:
		form = SignupForm()
	context = {
		'pagetitle': 'Create Account',
		'title': 'Create an account',
		'buttontext': 'Create Account',
		'form': form,
	}
	return render(request, 'login.html', context)

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('competition:signin'))