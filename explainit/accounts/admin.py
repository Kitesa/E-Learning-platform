from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import (Account, 
							TermsOfService,
							ProfilePic,
							UserBio,
							)
#MODEL REGISTRATIONS TO ADMIN
class AccountAdmin(UserAdmin):
	list_display 	= ('email', 'Phone_Number', 'date_joined', 
					'last_login', 'is_admin', 'is_active')
	search_fields 	= ('email', 'Phone_Number', 'username')
	readonly_fields	= ('date_joined', 'last_login')
	filter_horizontal	=()
	list_filter		=()
	fieldsets		=()
	
admin.site.register(Account, AccountAdmin)
admin.site.register(TermsOfService)
admin.site.register(ProfilePic)
admin.site.register(UserBio)