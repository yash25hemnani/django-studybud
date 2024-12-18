from django.contrib import admin
from django.urls import path
from . import views

urlpatterns= [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name="home"),
    path('room/', views.room_function, name="room_function"),
    path('room/<str:id>/', views.solo_room, name="solo_room"),
    path('profile/<str:id>/', views.userProfile, name="user_profile"),
    path('create-room/', views.createRoom, name="create_room"),
    path('update-room/<str:id>', views.updateRoom, name="update_room"),
    path('delete-room/<str:id>', views.deleteRoom, name="delete_room"),
    path('edit-message/<str:roomid>/<str:id>', views.editMessage, name="edit-message"),
    path('delete-message/<str:id>', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update_user"),

]

