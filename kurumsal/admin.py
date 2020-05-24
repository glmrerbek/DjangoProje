from django.contrib import admin
from kurumsal.models import Category, Images, Kurumsal

class KurumsalImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    list_filter = ['status'] #filtrelemek istediğimiz yöntemi belirtiyoruz
    readonly_fields = ( 'image_tag', )

class KurumsalAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status','image_tag']
    list_filter = ['status','category']
    inlines = [KurumsalImageInline]
    readonly_fields = ( 'image_tag', )

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'kurumsal','image_tag']
    readonly_fields = ( 'image_tag', )

admin.site.register(Category,CategoryAdmin)
admin.site.register(Kurumsal,KurumsalAdmin)
admin.site.register(Images,ImagesAdmin)
# Register your models here.
#admin panelde kategorilerin nasıl görüntüleneceğini falan bu sayfada ayarlıyoruz