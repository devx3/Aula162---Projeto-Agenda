from django.contrib import admin
from .models import Category, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'phone',
                    'email', 'created_at', 'category', 'enabled')
    list_display_links = ('firstname', 'lastname')
    search_fields = ['firstname', 'lastname', 'phone', 'email']
    list_filter = ['category']
    list_per_page = 5
    list_editable = ['email', 'phone', 'enabled']


admin.site.register(Category)
