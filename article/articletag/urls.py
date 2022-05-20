from articletag import views
from django.contrib import admin
from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static  

urlpatterns = [
    path('',views.homepage),
    path('homepage/',views.homepage),
    path('usersignup/',views.usersignup),
    path('userlogin/',views.userlogin),
    path('userlogout/',views.userlogout),    
    path('createarticle/',views.createarticle),
    path('editarticle/<int:id>',views.editarticle),
    path('deletearticle/<int:id>',views.deletearticle),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)