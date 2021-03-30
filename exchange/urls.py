from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name = 'register'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name = 'logout'),
    path('profile/', user_views.profile, name = 'profile'),
    path('trade/', user_views.trade , name ='trade'),
    path('', auth_views.LoginView.as_view(template_name = 'user/login.html'), name = 'login'),
    path('', include('app.urls'))
]