from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/', views.user_login, name='login'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'), 
    path('profile/', views.profile, name='profile'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('delete_blog/<int:post_id>/', views.delete_blog, name='delete_blog'),
    path('create_blog/', views.create_blog_post, name='create_blog'),
    path('blog_list/', views.blog_list, name='blog_list'),
]
