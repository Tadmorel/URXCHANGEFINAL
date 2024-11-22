# main/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),  # Página principal con login
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('universidad/<int:university_id>',views.university, name='university'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # Ruta para editar la publicación
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='main/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='main/password_change_done.html'), name='password_change_done'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Ruta para desactivar publicación
    path('password_recovery/', views.password_recovery, name='password_recovery'), #Ruta para cambiar contraseña
    path('reset-password/', views.reset_password, name='reset_password'),  # Agregar esta ruta
    path('delete_university/<int:university_id>/', views.delete_university, name='delete_university'),
    path('universidad/<int:university_id>/editar/', views.edit_university, name='edit_university'),
    path('delete_valuation/<int:comment_id>/', views.delete_valuation, name='delete_valuation'),
    path('profile/', views.profile_view, name='profile'),




]


