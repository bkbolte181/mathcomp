from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class SiteUserManager(BaseUserManager):
	def _create_user(self, email, password, first_name=None, last_name=None, department=None, school=None, lab=None, pi=None, research_interest=None, **extra_fields):
		if not email:
			raise ValueError('An email must be provided to create the user.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, first_name=None, last_name=None, department=None, school=None, lab=None, pi=None, research_interest=None, **extra_fields):
		return self._create_user(email, password)

	def create_superuser(self, email, password, first_name=None, last_name=None, department=None, school=None, lab=None, pi=None, research_interest=None, **extra_fields):
		return self._create_user(email, password)

	def get_by_natural_key(self, username):
		""" Allow Case-Insensitive Username. """
		return self.get(email__iexact=username)

class SiteUser(AbstractBaseUser):
	email = models.EmailField('email address', max_length=200, unique=True,
		error_messages={
			'unique': 'A user with that email already exists.',
		}, help_text="Emory Email Address")
	first_name = models.CharField(max_length=100, help_text="First Name")
	last_name = models.CharField(max_length=100, help_text="Last Name")
	
	is_staff = models.BooleanField(default=False)
	
	objects = SiteUserManager()

	# Required for custom user model
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def get_full_name(self):
		return self.first_name, self.last_name

	def get_short_name(self):
		return self.first_name
	
	email = models.EmailField('email address', max_length=200, unique=True,
		error_messages={
			'unique': 'A user with that email already exists.',
		}, help_text="Emory Email Address")

class Announcement(models.Model):
	title = models.CharField(max_length=100)
	message = models.TextField(max_length=10000)
	created_at = models.DateTimeField(auto_now_add=True, default=None)