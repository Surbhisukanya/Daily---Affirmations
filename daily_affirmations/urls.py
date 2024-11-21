from django.contrib import admin
from django.urls import path
from affirmations_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Added logout URL
    path('register/', views.register, name='register'),
    path('search/', views.search_affirmations, name='search'),
    path('suggest/', views.suggest_affirmation, name='suggest_affirmation'),
    path('profile/', views.profile, name='profile'),
]
