from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MotoUser, Owners

class OwnersInline(admin.StackedInline):
    model = Owners
    extra = 0

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', )
    list_filter = ('groups',)
    filter_horizontal = ('motobike',)
    inlines = (
        OwnersInline,
    )
# Добавляем поле с биографией 
# к стандартному набору полей (fieldsets) пользователя в админке.
#UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где под ключом fields можно указать нужные поля.
    #('Extra Fields', {'fields': ('moto', )}),
#)
# Регистрируем модель в админке:
admin.site.register(MotoUser, UserAdmin)
