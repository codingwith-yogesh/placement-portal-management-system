from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home, name='home'),
    
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
    
    path(
        'company/dashboard/',
        views.company_dashboard,
        name='company_dashboard'
    ),
    
    path(
        'profile/',
        views.profile,
        name='profile'
    ),
    
    path(
        'login/',
        views.custom_login,
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    
    path(
        'company/register/',
        views.company_register,
        name='company_register'
    ),
    
    path(
        'job/create/',
        views.create_job,
        name='create_job'
    ),

    path(
        'jobs/',
        views.job_list,
        name='job_list'
    ),

    path(
        'apply/<int:job_id>/',
        views.apply_job,
        name='apply_job'
    ),
    
    path(
        'my-applications/',
        views.my_applications,
        name='my_applications'
    ),

    path(
        'company/applicants/',
        views.company_applicants,
        name='company_applicants'
    ),
    
    path(
        'application/<int:app_id>/<str:status>/',
        views.update_status,
        name='update_status'
    ),
    
    path(
        'upload-resume/',
        views.upload_resume,
        name='upload_resume'
    ),
    
    path(
        'analytics/',
        views.analytics,
        name='analytics'
    ),
    
    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),
    
    path(
        'job/edit/<int:job_id>/',
        views.edit_job,
        name='edit_job'
    ),
    
    path(
        'job/delete/<int:job_id>/',
        views.delete_job,
        name='delete_job'
    ),
    
]