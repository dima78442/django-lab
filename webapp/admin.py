from django.contrib import admin
from .models import Person, Phone


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'address', 'birth_date')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('id', 'first_name', 'last_name', 'address')


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'phone_number', 'active', 'date')
    list_display_links = ('id', 'phone_number')
    search_fields = ('phone_number', 'person')
    list_filter = ('person',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Phone, PhoneAdmin)
