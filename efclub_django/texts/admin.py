from django.contrib import admin
from texts.models import Channel, User, UserStatus, Text, Group, GetcourseGroup, MessageNewStatus
# Register your models here.
# from models import UserStatus

# TODO проверить все имена
# class UserStatusAdmin(admin.ModelAdmin):
#     pass


class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'telegram_id', 'status', 'expiration_date', ]
    list_filter = ['got_invite', 'status']
    search_fields = ['phone']


class TextAdmin(admin.ModelAdmin):
    pass


class MessageNewStatusAdmin(admin.ModelAdmin):
    pass
    # list_display = ['user_name', 'short_text', 'news']
    # list_filter = ['user_name']

    # actions = ['delete_comment']

    # def short_text(self, obj):
    #     # return f'{obj.text[:15]}{"..." if len(obj.text) > 15 else ""}'
    #     return Truncator(obj.text).chars(15)
    #
    # def delete_comment(self, request, queryset):
    #     queryset.update(text='Удалено администратором')
    #
    # delete_comment.short_description = 'Удалить комментарий'
    # short_text.short_description = 'Текст комментария'


# admin.site.register(UserStatus, UserStatusAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(MessageNewStatus, MessageNewStatusAdmin)
admin.site.register(User, UserAdmin)
