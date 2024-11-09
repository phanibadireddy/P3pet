"""
URL configuration for petshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pawsnclaws import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.open),
    path('home',views.first),
    path('sign',views.reg ,name='sign'),
    path('fp',views.forget),
    path('changepass',views.change_password),
    path('login',views.login),
    path('profile',views.profile),
    path('opro',views.opro),
    path('shopadd', views.adreg),
    path('ad', views.adplace),
    path('success',views.payment),
    path('shopreg',views.shopreg),
    path('adp',views.adreg),
    path('search',views.ser),
    path('find',views.show),
    path('sout',views.logout),
    path('ap',views.ap),
    path('make-payment', views.make_payment, name='make_payment'),
    path('ts',views.tsell),
    path('tb',views.tbuy),
    path('delete-item/', views.delete_item, name='delete_item'),
    path('cad',views.adadress),
    path('Add',views.add_address),
    path('b', views.adr, name='select_item'),
    path('send_request/<int:address_id>/', views.send_request, name='send_request'),
    path('ureq',views.ure),
    path('req',views.sreq),
    path('accept-request/', views.accept_request, name='accept_request'),
    path('reject-request/', views.reject_request, name='reject_request'),
    path('afreq',views.afterorder),
    path('succ',views.ap),
    path('shop-complaints',views.complaint),
    path('feedback',views.feedback),
    path('comp',views.submit_complaint),
    path('send-warning/', views.send_warning, name='send_warning'),
    path('shadd',views.showadd),
    path('remove-user/', views.remove_user, name='remove_user'),
    path('tad',views.shfulladd),
    path('delete-ad/',views.delete_ad),
    path('ost',views.orderstatus),
    path('delete-seller',views.remove_user),
    
    
    

    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

