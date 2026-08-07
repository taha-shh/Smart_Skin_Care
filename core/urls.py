from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from skincare import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('login/', views.login_page, name='login'),
    path('products/', views.products_page, name='products'),
    path('register/', views.register_page, name='register'),   
    path('upload/', views.upload_skin_image, name='upload_skin_image'),
    path('chat/', views.skin_chat_bot, name='skin_chat_new'),
    path('chat/<int:session_id>/', views.skin_chat_bot, name='skin_chat_session'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)