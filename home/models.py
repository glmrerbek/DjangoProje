from django.db import models
from ckeditor_uploader.fields import  RichTextUploadingField
from django.forms.widgets import TextInput, Textarea
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
class Setting(models.Model):
    STATUS=(
        ('1', 'Evet'),
        ('0', 'Hayir')
    )
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    keywords= models.CharField(max_length=255)
    company = models.CharField(max_length=150)
    address = models.CharField(blank= True, max_length=100)
    phone = models.CharField(blank= True, max_length=15)
    fax = models.CharField(blank= True, max_length=15)
    email = models.CharField(max_length=20)
    smtpserver = models.CharField(blank= True,max_length=20)
    smtpemail = models.CharField(blank= True,max_length=30)
    smtppassword = models.CharField(max_length=150)
    smtpport = models.CharField(blank= True, max_length=5)
    icon = models.ImageField(blank= True, upload_to ='images/' )
    facebook = models.CharField(blank= True,max_length=150)
    instagram = models.CharField(blank= True,max_length=150)
    twitter = models.CharField(blank= True,max_length=150)
    about = RichTextUploadingField(blank= True)
    contact = RichTextUploadingField(blank= True)
    references = RichTextUploadingField(blank= True)
    status= models.CharField(max_length=10, choices=STATUS)
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
    )
    name= models.CharField(blank=True, max_length=20)
    email= models.CharField(blank=True, max_length=50)
    subject= models.CharField(blank=True, max_length=50)
    message= models.CharField(blank=True, max_length=255)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name' : TextInput (attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject' : TextInput (attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email' : TextInput (attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message' : Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class UserProfile(models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return   self.user.first_name + ' ' + self.user.first_name + ' [' +self.user.username + '] ' 

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileFormu(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']
