from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import contacts.views

urlpatterns = patterns('',
                url(r'^$', contacts.views.ListContactView.as_view(),
                    name='contacts-list',),
                url(r'^new$', contacts.views.CreateContactView.as_view(),
                    name='contacts-new',),
    # Examples:
    # url(r'^$', 'addressbook.views.home', name='home'),
    # url(r'^addressbook/', include('addressbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
