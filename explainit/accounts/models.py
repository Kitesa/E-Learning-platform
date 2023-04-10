from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import Image  


class Gender(models.Model):
	'''
		A MODEL FOR GENDER OF USER ONLY SUPER USER 
		HAVE PERMISSION TO INTERACT WITH THIS MODEL
	'''
	gender_option= models.CharField(max_length=10)

	def __str__(self):
		return str(self.gender)


class UserAccountManager(BaseUserManager):
	'''
		A CUSTOM ACCOUNTS MODEL MANAGER TO MANAGE USER ACCOUNT
		BY TESTING USER INFORMATION FOR REQUIREMENT OF THE REGISTRATION.
	'''
	def create_user(self, email, username, first_name, last_name, Phone_Number, password=None):
		"""
			A FUNCTION TO TEST USER REGISTRATION FOR 
			DIFFERENT REQUIREMENT OF THE PLATFORM
		"""
		if not email:
			raise ValueError('No email address!')
		if not username:
			raise ValueError('No username!')

		user = self.model(
			email           = self.normalize_email(email),
			username        = username,
			first_name      = first_name,
			last_name       = last_name,
			Phone_Number    = Phone_Number,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name, last_name, Phone_Number, password):
		"""
			A FUNCTION TO TEST SUPERUSER CREATION FOR DIFFERENT 
			REQUIREMENT OF THE PLATFORM
		"""
		user = self.create_user(
            email           = self.normalize_email(email),
            password        = password,
            username        = username,
            first_name      = first_name,
            last_name       = last_name,
            Phone_Number    = Phone_Number,
		)
		user.is_admin       = True
		user.is_staff       = True
		user.is_superuser   = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser, PermissionsMixin):
	'''
		custom user account model
	'''
	first_name              		= models.CharField(max_length=30)
	last_name               		= models.CharField(max_length=30)
	email                   		= models.EmailField(verbose_name="Email", max_length=70, unique=True)
	Phone_Number            		= models.CharField(verbose_name="Phone Number", max_length=15, unique=True)
	username                		= models.CharField(max_length=30, unique=True)
	birth_date                      = models.DateTimeField(null=True)
	date_joined             		= models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
	last_login              		= models.DateTimeField(verbose_name='Last Login', auto_now=True)
	gender                  		= models.ForeignKey(Gender, related_name='gender', on_delete=models.CASCADE, null=True, blank=True)
	is_admin                		= models.BooleanField(default=False)
	is_active               		= models.BooleanField(default=True)
	is_staff                		= models.BooleanField(default=False)
	is_our_teacher 					= models.BooleanField(default=False)
	is_individual_user              = models.BooleanField(default=True)



	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'Phone_Number']

	objects = UserAccountManager()

	def __str__(self):
		'''
		A function that returns string representation of an object
		'''
		return self.username

    
	def has_perm(self, perm, obj=None):
		'''
		A function For checking permissions. 
		all admin have ALL permissons
		'''
		return self.is_admin


	def has_module_perms(self, app_label):
		'''
		 A function that checks if this user have permission to view this app
		 it is set to yes in xplainit rule
		 '''
		return True

    
	def full_name(self):
		'''
		A function tjhat returns full name of the user
		by concatenating first and last name of the user
		'''
		return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'


	def get_absolute_url(self):
		'''
		where the page should rdirect to after successful creation of 
		user account - user is redirected to home page in explainit rule
		'''
		return reverse('/')


