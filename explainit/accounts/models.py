from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import Image  
from ckeditor.fields import RichTextField 
from django.conf import settings
from io import BytesIO
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile

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
	gender                  		= models.CharField(max_length=5, null=False, blank=False, default='M')
	is_admin                		= models.BooleanField(default=False)
	is_active               		= models.BooleanField(default=False)
	is_staff                		= models.BooleanField(default=False)
	is_our_teacher 					= models.BooleanField(default=False)
	followers 						= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='account_followers', blank=True)
	
	@property
	def total_followers(self):
		return self.followers.count()

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

	@property
	def full_name(self):
		'''
		A function that returns full name of the user
		by concatenating first and last name of the user
		'''
		return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'


	def get_absolute_url(self):
		'''
		where the page should rdirect to after successful creation of 
		user account - user is redirected to home page in explainit rule
		'''
		return reverse('accounts:user-profile-home-view')


def profile_pic_upload_filepath(self, filename):
	'''
	A function that returns the file sytem path to which the user
	profile picture should be uploaded
	'''
	return f'profile_pictures/{self.user.username}/{"profile_pictures.jpeg"}'


class ProfilePic(models.Model):
	user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_pic')
	image           = models.ImageField(default='default.png', upload_to=profile_pic_upload_filepath)

	def __str__(self):
		return f'{self.user.username} Profile picture'

	def save(self, **kwargs):
		super().save()
		try:
			if self.image.url:
				img_read = storage.open(self.image.name, "r")
				img = Image.open(img_read)
				if img.height > 400 or img.width > 400:
					output_size = (400, 400)
					imageBuffer = BytesIO()
					img.thumbnail(output_size)
					img = img.convert('RGB')
					img.save(imageBuffer, 'jpeg')

					user = Account.objects.get(pk=self.user.pk)
					user.profile_pic.image.save(self.image.name, ContentFile(imageBuffer.getvalue()))
		except:
			print("doesnot exist")
	def get_absolute_url(self):
		'''
		A function that returns where the page should redirect to
		After successful upload of profile picture
		'''
		return reverse('accounts:user-profile-home-view')


class TermsOfService(models.Model):
	"""
		A DB MODEL CLASS TO STORE TERMS OF SERVICES
		RULES AND REGULATIONS THAT OUR USER NEED TO AGREE WITH
	"""

	title                   = models.CharField(max_length = 254)
	terms_of_service        = RichTextField()

	def __str__(self):
		return self.title


class OurTeacherProfile(object):
	"""
		A DB MODEL CLASS TO HOLD INFORMATION ABOUT OUR
		TEACHERS
	"""
	

class UserBio(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bios')
	bio  = RichTextField()

	def __str__(self):
		return f'{self.user.full_name}-bio'