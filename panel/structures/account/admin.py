from django.contrib import admin
from .models import (UserType, Profile, Role, Address, Phone,
	Company, Brand)

class UserTypeAdmin(admin.ModelAdmin):
	pass

class ProfileAdmin(admin.ModelAdmin):
	pass

class RoleAdmin(admin.ModelAdmin):
	pass

class AddressAdmin(admin.ModelAdmin):
	pass

class PhoneAdmin(admin.ModelAdmin):
	pass

class CompanyAdmin(admin.ModelAdmin):
	pass

class BrandAdmin(admin.ModelAdmin):
	pass



admin.site.register(UserType, UserTypeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Brand, BrandAdmin)