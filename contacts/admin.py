from contacts.models import *
from django.contrib import admin


class DonationInline(admin.TabularInline):
    model = Donation
    # fields = ['amount', 'type', 'date']
    readonly_fields = ['date']
    extra = 1

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'get_tags')
    search_fields = ['first_name', 'last_name', 'tags__tag']
    inlines = [NoteInline, DonationInline]

admin.site.register(Tag)
admin.site.register(Contact, ContactAdmin)
