from django.contrib import admin
from .models import Category, Location, Post, Comments
admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )    
    search_fields = ('title',) 
    list_filter = ('is_published',)
    list_display_links = (
        'title',
        'description',
    )

class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )    
    search_fields = ('name',) 
    list_filter = ('is_published',)
    list_display_links = (
        'name',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'category',
        'location',
        'pub_date',
        'is_published',
        
    )
    list_editable = (
        'is_published',
    )    
    search_fields = (
        'author',
        'title',
        'category',
        'location',
    ) 
    list_filter = ('is_published',)
    list_display_links = (
        'author',
        'title',
    )   

admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments)