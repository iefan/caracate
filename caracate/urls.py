from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import logout
from caracate.views import myuser_login

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'caracate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^logout/$', logout,{'template_name':'logout.html'}),
    url(r'^login/$', myuser_login,  {'template_name': 'login.html'}),

)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
