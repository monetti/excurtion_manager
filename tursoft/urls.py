from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import list_detail
from excurtionManager.models import Product, Excurtion, Client, Notification
from tursoft import settings
import datetime

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

#Vistas Genericas
product_list = {
                'queryset':Product.objects.filter(excurtion__date_to__lte=datetime.datetime.today()),
                'allow_empty':True,
                }

excurtion_list = {
                'queryset':Excurtion.objects.all(),
                'allow_empty':True,
                }

client_list = {
                'queryset':Client.objects.all(),
                'allow_empty':True,
                }

notification_list = {
                'queryset':Notification.objects.all(),
                'allow_empty':True,
                }


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tursoft.views.home', name='home'),
    url(r'^register/$', 'tursoft.views.register', name='register'),
    url(r'^login/$', 'tursoft.views.login', name='login'),
        
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^products/$', list_detail.object_list, product_list),
    url(r'^excurtions/$', list_detail.object_list, excurtion_list),
    url(r'^clients/$', list_detail.object_list, client_list),
    url(r'^notifications/$', list_detail.object_list, notification_list),
    
    url(r'^products/(?P<id>\w+)$', 'excurtionManager.views.detail_product'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.STATIC_ROOT}),
    )
