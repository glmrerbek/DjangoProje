from django.contrib import admin
from home.models import ContactFormMessage, Setting, UserProfile

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','subject']
    list_filter = ['status'] #filtrelemek istediğimiz yöntemi belirtiyoruz

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','address','city','country', 'image_tag']

admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(Setting)
admin.site.register(UserProfile,UserProfileAdmin)