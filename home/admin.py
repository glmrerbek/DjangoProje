from django.contrib import admin
from home.models import Setting, ContactFormMessage

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','subject']
    list_filter = ['status'] #filtrelemek istediğimiz yöntemi belirtiyoruz

admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(Setting)