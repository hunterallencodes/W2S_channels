from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from chat.views import Login

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]
