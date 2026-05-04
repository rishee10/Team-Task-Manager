from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('members/', views.members_list, name='members'),
    path('members/<int:user_id>/toggle-role/', views.toggle_role, name='toggle_role'),
]
