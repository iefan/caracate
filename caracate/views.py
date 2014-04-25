from django.contrib.auth.views import login
def myuser_login(request, *args, **kwargs):
    if request.method == 'POST':
        request.session.set_expiry(6000) #设置 cookie 时间 10 分钟
        # if not request.POST.get('remember', None):
        #     request.session.set_expiry(0)
 
    return login(request, *args, **kwargs)