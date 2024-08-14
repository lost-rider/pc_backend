from django.urls import path, re_path
from django.contrib import admin
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login',views.login),
    re_path('signup',views.signup),

    
]
