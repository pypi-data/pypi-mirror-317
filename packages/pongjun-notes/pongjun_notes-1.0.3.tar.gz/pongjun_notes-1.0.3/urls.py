from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:note_id>/update/', views.update, name='update'),
    path('<int:note_id>/delete/', views.delete, name='delete'),
    path('datetime/', views.show_datetime, name='show_datetime'),
    path('directory/', views.show_directory_listing, name='show_directory_listing'),
    
]
