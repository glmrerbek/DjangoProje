from django.contrib import admin
from kurumsal.models import Category, Comment, Images, Kurumsal
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from django.forms import ModelForm


class KurumsalImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title', 'status','image_tag']
    list_filter = ['status'] #filtrelemek istediğimiz yöntemi belirtiyoruz
    readonly_fields = ( 'image_tag', )

class KurumsalAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status','image_tag']
    list_filter = ['status','category']
    inlines = [KurumsalImageInline]
    readonly_fields = ( 'image_tag', )
    prepopulated_fields = {'slug': ('title',)}

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'kurumsal','image_tag']
    readonly_fields = ( 'image_tag', )

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_kurumsals_count', 'related_kurumsals_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Kurumsal,
                'category',
                'kurumsals_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Kurumsal,
                 'category',
                 'kurumsals_count',
                 cumulative=False)
        return qs

    def related_kurumsals_count(self, instance):
        return instance.kurumsals_count
    related_kurumsals_count.short_description = 'Related kurumsals (for this specific category)'

    def related_kurumsals_cumulative_count(self, instance):
        return instance.kurumsals_cumulative_count
    related_kurumsals_cumulative_count.short_description = 'Related kurumsals (in tree)'


# Register your models here.
#admin panelde kategorilerin nasıl görüntüleneceğini falan bu sayfada ayarlıyoruz

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'kurumsal', 'user','status']
    list_filter = ['status']


admin.site.register(Category,CategoryAdmin2)
admin.site.register(Kurumsal,KurumsalAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register (Comment, CommentAdmin)
