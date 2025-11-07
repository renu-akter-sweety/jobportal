from django.urls import path
from job_portal_app.views import *

urlpatterns = [
    path('register/',register_func, name='register_func'),
    path('',login_func, name='login_func'),
    path('logout/',logout_func, name='logout_func'),
    
    path('dashboard/',dashboard, name='dashboard'),
    path('profile/',profile,name='profile'),
    path('update-profile/',update_profile, name='update_profile'),
    
    path('job-list/',job_list, name='job_list'),
    path('add-job/',add_job, name='add_job'),
    path('update-job/<int:job_id>/',update_job, name='update_job'),
    path('delete-job/<int:job_id>/',delete_job, name='delete_job'),
    
    path('apply-job/<int:job_id>/',applied_job, name='applied_job'),
    path('my-applications/',my_application,name='my_application'),
    
    path('applicant-list/<int:job_id>/',applicant_list,name='applicant_list'),
    path('shortlisted/<int:applied_id>/',shortlisted, name='shortlisted'),
    path('rejected/<int:applied_id>/',rejected, name='rejected'),
]
