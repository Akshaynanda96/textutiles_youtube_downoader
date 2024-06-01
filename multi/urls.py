
from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('analyze/', views.analyze, name='analyze'),
    path('youtube_url/', views.yputube_url , name='youtube_url'),
    path('Download/', views.youtube_download , name='youtube_download'),
    path('download_video/', views.download_video, name='download_video'),

]
