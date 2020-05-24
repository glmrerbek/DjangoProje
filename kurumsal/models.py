from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import  RichTextUploadingField

# Create your models here.
class Category (models.Model):
    STATUS = (
        (1, 'Evet'),
        (0, 'Hayır')
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.IntegerField(choices=STATUS)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title
#blank=True birşey boş kabul edilebilir mesela parent kısmı boş olabilir
#iki amacı vardır bu yapının hem açılır pencerede tablo oluşturur hemde adminde yönetimi sağlanır
#kategoride isim yazarak arama yapmayı sağlar

class Kurumsal(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayir')
    )
    category=models.ForeignKey (Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    keywords= models.CharField(max_length=255)
    image= models.ImageField(blank= True, upload_to ='images/' )
    status= models.CharField(max_length=10, choices=STATUS)
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    detail= RichTextUploadingField()
    slug=models.SlugField()
    parent =models.ForeignKey('self', blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Images(models.Model):
    kurumsal=models.ForeignKey (Kurumsal, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank= True)
    image= models.ImageField(blank= True, upload_to ='images/' )
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
