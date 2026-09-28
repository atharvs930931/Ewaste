from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),   # 👈 VERY IMPORTANT
    path('logout/', views.logout_view, name='logout'),
    path('submit/', views.submit_ewaste, name='submit_ewaste'),
    path('accept/', views.accept_ewaste, name='accept_ewaste'),
    path('accept/<int:ewaste_id>/', views.accept_request, name='accept_request'),
    path('status/', views.status_tracking, name='status_tracking'),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    
]
