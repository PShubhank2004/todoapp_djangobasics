
from django.contrib import admin
from django.urls import path
from .  import views
urlpatterns = [
    path('',views.signup,name ='signup'),
    path('login/',views.login_view,name ='login'),
    path('main/',views.main,name='main'),
    path('logout/', views.loggingout, name='logout'),
    path('edit-task/<int:pk>/',views.edit_task, name='edit-task'),
    path('delete/<int:pk>/', views.delete_task, name='delete-task'),
]
