from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_bill, name='add'),
    path('my-bills/', views.bill_list, name='bill_list'),
    path('delete/<int:id>/', views.delete_bill, name='delete_bill'),
    path("extend/<int:id>/", views.extend_warranty, name='extend_warranty'),
    path('send-notifications/', views.trigger_notifications),
]




