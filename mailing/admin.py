from django.contrib import admin

# Register your models here.

from mailing.models import Client, Mailing, Message, Code, Tag, UserProfile

admin.site.site_header = u'Admin panel'
admin.site.index_title = u'Manage your mailings'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ('phone_number', 'operator_code', 'tag', 'timezone',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    fields = ('start_at', 'text', 'operator_code', 'tag', 'finish_at',)    

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ('status', 'maillist', 'customer',)

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    fields = ('code',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)



