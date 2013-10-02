from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import contacts.views as cv

urlpatterns = patterns('',
                url(r'^hello$', cv.HelloWorld,
                    name='hello-world'),
                url(r'^date$', cv.CurDateTime,
                    name='hello-world'),
                url(r'^date/(\d+)$', cv.FutureDateTime,
                    name='hello-world'),
                url(r'^receipt/(?P<slug>\w+)$', cv.ReceiptView.as_view(),
                    name='receipt'),
                url(r'^$', cv.ListContactView.as_view(),
                    name='contacts-list',),
                url(r'^new$', cv.CreateContactView.as_view(),
                    name='contacts-new',),
    # Examples:
    # url(r'^$', 'addressbook.views.home', name='home'),
    # url(r'^addressbook/', include('addressbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
