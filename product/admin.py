import admin_thumbnails
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin


from product.models import Category, Product, Images, Comment, Variants, Color, Size, GoesWellWith, WishList, \
    SearchHistory, Reply


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'



@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class GoesWellWithInline(admin.TabularInline):
    model = GoesWellWith
    readonly_fields = ('image_tag',)
    extra = 1
    fk_name = "product"
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag', 'avaregereview']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline, ProductVariantsInline,
               GoesWellWithInline
               ]
    prepopulated_fields = {'slug': ('title',)}

class CommenttoReplyInline(admin.TabularInline):
    model = Reply
    readonly_fields = ('reply','ip','user','id')
    can_delete = False
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status', 'create_at']
    readonly_fields = ('subject','comment','ip','user','product','rate','id')
    inlines = [CommenttoReplyInline]


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['parentComment', 'reply', 'status','create_at']
    list_filter = ['status', 'create_at']
    readonly_fields = ('ip','user','id')


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']


class GoesWellWithAdmin(admin.ModelAdmin):
    list_display = ['product', 'goeswellwith', 'image_tag']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_tag','user']
    list_filter = ['user',]

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_tag', 'user', 'timestamp', 'searchedNow']
    list_filter = ['user', 'searchedNow']


admin.site.register(Category,CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(GoesWellWith, GoesWellWithAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)

admin.site.register(Reply, ReplyAdmin)

