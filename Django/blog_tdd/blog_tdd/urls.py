from django.conf.urls import patterns, include, url
from blog import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog_tdd.views.home', name='home'),
    # url(r'^blog_tdd/', include('blog_tdd.foo.urls')),
    url(r'^', include('blog.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.home),
    url(r'^admin/', include(admin.site.urls)),
)
