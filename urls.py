from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MiniMicroBlog.views.home', name='home'),
    # url(r'^MiniMicroBlog/', include('MiniMicroBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$','microblog.views.login'),
    url(r'^login/$','microblog.views.login'),
    url(r'^logout/$','microblog.views.logout'),
    #url(r'^home/$','microblog.views.loadhome'),
    url(r'^home/(?P<pageindex>\d+)/$','microblog.views.loadhome'),
    #url(r'^square/$','microblog.views.loadsquare'),
    url(r'^square/(?P<pageindex>\d+)/$','microblog.views.loadsquare'),
    #url(r'^find/$','microblog.views.loadusers'),
    #url(r'^find/follow/?P<username>[a-zA-Z-_\d]+/$','microblog.views.addfriend'),
    #url(r'^find/unfollow/?P<username>[a-zA-Z-_\d]+/$','microblog.views.deletefriend'),
    url(r'^find/(?P<pageindex>\d+)/$','microblog.views.loadusers'),
    url(r'^register/$','microblog.views.signup'),
    url(r'^register/success/$','django.views.generic.simple.direct_to_template',
        {'template':'prompt/resetsuccess.html'}),
    url(r'^reset/$','microblog.views.sendpwd'),
    url(r'^reset/success/$','django.views.generic.simple.direct_to_template',
            {'template':'prompt/resetsuccess.html'}),
    url(r'^help/$','django.views.generic.simple.direct_to_template',
            {'template':'help/aboutweb.html'}),
    url(r'^help/aboutme/$','django.views.generic.simple.direct_to_template',
            {'template':'help/aboutme.html'}),
    url(r'^help/webstate/$','django.views.generic.simple.direct_to_template',
            {'template':'help/webstate.html'}),
    url(r'^user/publish/$','microblog.views.publish'),
    url(r'^user/setting/$','microblog.views.setting'),
    url(r'^user/changepwd/$','microblog.views.changepwd'),
    url(r'^user/follow/(?P<pageindex>\d+)/$','microblog.views.loadfollowuser'),
    url(r'^user/(?P<username>[\w_\d]+)/(?P<pageindex>\d+)/$','microblog.views.loadusershuoshuo'),
    url(r'^message/(?P<ssid>\d+)/$','microblog.views.ssdetail'),
    url(r'^prompt/(?P<way>\bfollow\b)/(?P<param>[\w_\d]+)/$','microblog.views.systeminfo'),
    url(r'^prompt/(?P<way>\bunfollow\b)/(?P<param>[\w_\d]+)/$','microblog.views.systeminfo'),
    url(r'^prompt/(?P<way>\bdelshuoshuo\b)/(?P<param>[\w_\d]+)/$','microblog.views.systeminfo'),
    url(r'^admin/', include(admin.site.urls)),
)
