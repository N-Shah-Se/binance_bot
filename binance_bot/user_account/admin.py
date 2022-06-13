from django.contrib import admin
from .models import Profile

# admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "password", "phone", "is_active", "invitation_code")
admin.site.register(Profile, ProfileAdmin)

# Register your models here.
