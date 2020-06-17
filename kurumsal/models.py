from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import  RichTextUploadingField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from random import choices
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.forms.widgets import FileInput, Select, TextInput
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm
# Create your models here.
class Category(MPTTModel):
    STATUS = (
        (1, 'Evet'),
        (0, 'Hayır')
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.IntegerField(choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    detail= RichTextUploadingField(blank= True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    parent =TreeForeignKey('self', blank=True, null=True ,related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
    
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[ ::-1])


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

#blank=True birşey boş kabul edilebilir mesela parent kısmı boş olabilir
#iki amacı vardır bu yapının hem açılır pencerede tablo oluşturur hemde adminde yönetimi sağlanır
#kategoride isim yazarak arama yapmayı sağlar


TYPE = (
    ('haber', 'haber'),
    ('duyuru', 'duyuru'),
    ('etkinlik', 'etkinlik'),
)

class Kurumsal(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayir')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    keywords= models.CharField(max_length=255)
    image= models.ImageField(upload_to ='images/' )
    type = models.CharField(max_length=10, choices=TYPE)
    status= models.CharField(max_length=10, choices=STATUS)
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    detail= RichTextUploadingField(blank= True)
    slug=models.SlugField(null=False, unique=True)
    parent =models.ForeignKey('self', blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('kurumsal_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    kurumsal=models.ForeignKey (Kurumsal, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank= True)
    image= models.ImageField(blank= True, upload_to ='images/' )
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS =(
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    kurumsal = models.ForeignKey( Kurumsal, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=200,blank=True)
    rate = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.subject

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
        

class ContentForm(ModelForm):
    class Meta:
        model = Kurumsal
        fields = ['type', 'category', 'title', 'slug', 'keywords',
                  'description', 'image', 'detail']
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'type': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=TYPE),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
            'detail': CKEditorWidget(),
        }


class ContentImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']
