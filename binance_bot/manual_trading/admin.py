from django.contrib import admin
from manual_trading.models import BotUser
# Register your models here.

# admin.site.register(BotUser)

class BotUserAdmin(admin.ModelAdmin):
    list_display = ("user", "api_key", "secret_key")
admin.site.register(BotUser, BotUserAdmin)