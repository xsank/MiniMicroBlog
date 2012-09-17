from django.contrib import admin
from microblog.models import *

class PostWayAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    list_per_page = 5


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','realname','email')
    list_display_links = ('username','realname','email')
    list_per_page = 10


class ShuoshuoAdmin(admin.ModelAdmin):
    list_display = ('id','postwayname','shortcut','username')
    list_display_links = ('id','shortcut')
    search_fields = ['message']
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','username','shortcut')
    list_display_links = ('id','shortcut')
    search_fields = ['comment']
    list_per_page = 10


class MsgTextAdmin(admin.ModelAdmin):
    list_display = ('id','senduser','msgtext','sendtime')
    list_display_links = ('id','msgtext')
    search_fields = ['msgtext']
    list_per_page = 10


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','recvuser','message','kind')
    list_display_links = ('id','message')
    search_fields = ['message']
    list_per_page = 10


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','kind')
    list_display_links = ('id','kind')
    list_per_page = 10


admin.site.register(Shuoshuo,ShuoshuoAdmin)
admin.site.register(PostWay,PostWayAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(MsgText,MsgTextAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Status,StatusAdmin)
