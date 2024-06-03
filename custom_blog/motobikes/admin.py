from django.contrib import admin
from .models import Motobike
admin.site.empty_value_display = 'Не задано'


class MotobikeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'manufacturer',
        'model',
    )
    list_editable = (
        'manufacturer',
        'model',
    )    
    search_fields = (
        'name',
        'manufacturer',
        'model',) 
    list_filter = ('manufacturer',)
    list_display_links = (

    )


admin.site.register(Motobike, MotobikeAdmin)