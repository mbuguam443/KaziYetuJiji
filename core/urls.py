from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('my-applications/', views.job_seeker_dashboard, name='job_seeker_dashboard'),

]
