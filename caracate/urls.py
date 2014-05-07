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
    url(r'^changepassword/$', 'keepeyes.views.changepassword'),
    url(r'^inituserpassword/$', 'keepeyes.views.inituserpassword'),

    url(r'^$', 'keepeyes.views.index'),
    url(r'^cc_select/$', 'keepeyes.views.cc_select'),
    url(r'^cc_input/$', 'keepeyes.views.cc_input'),
    url(r'^cc_modify/(\d+)/$', 'keepeyes.views.cc_modify'),

    url(r'^notcc_select/$', 'keepeyes.views.notcc_select'),
    url(r'^notcc_input/$', 'keepeyes.views.notcc_input'),
    url(r'^notcc_modify/(\d+)/$', 'keepeyes.views.notcc_modify'),

    url(r'^cc_approvallist/$', 'keepeyes.views.cc_approvallist'),
    url(r'^cc_approvalinput/(\d+)/$', 'keepeyes.views.cc_approvalinput'),
    url(r'^cc_onekeyapproval/$', 'keepeyes.views.cc_onekeyapproval'),

    url(r'^notfit_cc_approvallist/$', 'keepeyes.views.notfit_cc_approvallist'),
    url(r'^notfit_cc_approvalinput/(\d+)/$', 'keepeyes.views.notfit_cc_approvalinput'),
    url(r'^notfit_cc_onekeyapproval/$', 'keepeyes.views.notfit_cc_onekeyapproval'),

    url(r'^downloadfile_list/$', 'keepeyes.views.downloadfile_list'),
    url(r'^generate_downfiles/$', 'keepeyes.views.generate_downfiles'),
    url(r'^downfile_bnz/(.*)/$', 'keepeyes.views.downfile_bnz'),
    url(r'^cc_phone/$', 'keepeyes.views.cc_phone'),

    url(r'^gmx_list/$', 'keepeyes.views.gmx_list'),
    url(r'^gmx_input/$', 'keepeyes.views.gmx_input'),
    # url(r'^refresh/(.*)/$', 'mental.views.refresh'),

    # url(r'^cc_modify/(\d+)/$', 'keepeyes.views.cc_modify'),

)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
