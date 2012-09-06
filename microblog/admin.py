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

admin.site.register(Shuoshuo,ShuoshuoAdmin)
admin.site.register(PostWay,PostWayAdmin)
admin.site.register(User,UserAdmin)
