from django.urls import path
from userauth import views

urlpatterns=[
    path('login/', views.login, name='login'),
    path('searchuser/', views.searchUser, name= 'search-user'),
    path('<username>/', views.userProfile, name= 'profile'),
    path('<username>/saved/', views.userProfile, name= 'saved'),
    path('<username>/follow/', views.follow, name= 'follow'),
    path('<username>/editprofile', views.editProfile, name= 'editProfile'),
    path('accounts/register/', views.register, name='register'),
] 