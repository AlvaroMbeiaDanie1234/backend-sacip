from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('login', views.login_user),
    path('logout/', views.logout_user, name='logout'),
    path('organizational-units/', views.list_organizational_units, name='organizational-units-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/menu-permissions/', views.assign_menu_permissions, name='assign-menu-permissions'),
    path('users/<int:user_id>/menu-permissions/list/', views.get_user_menu_permissions, name='get-user-menu-permissions'),
    path('users/me/', views.get_current_user, name='current-user'),
    path('roles/', views.RoleListView.as_view(), name='role-list'),
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='role-detail'),
    path('menu-permissions/', views.MenuPermissionListView.as_view(), name='menu-permission-list'),
    path('menu-permissions/<int:pk>/', views.MenuPermissionDetailView.as_view(), name='menu-permission-detail'),
]