from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required, user_passes_test
from competition.forms import *

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