from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from job_portal_app.models import *
from django.contrib import messages

def register_func(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        
        username_exist = PortalUserModel.objects.filter(username = username).exists()
        
        if username_exist:
            return redirect('register_func')
        
        if password == conf_password:
            user = PortalUserModel.objects.create_user(
                username = username,
                email=email,
                user_type = user_type,
                password = password
            )
            
            if user_type == 'Employer':
                EmployerModel.objects.create(
                    employer = user
                )
            else:
                JobSeekerModel.objects.create(
                    seeker = user
                )
            return redirect('login_func')
        else:
            messages.error(request, 'Both password does not match')
            return redirect('register_func')
    
    return render(request, 'auth/register.html')

def login_func(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('login_func')
        
    return render(request, 'auth/login.html')

def dashboard(request):
    
    return render(request,'dashboard.html')

def logout_func(request):
    logout(request)
    return redirect('login_func')

def profile(request):
    
    return render(request, 'profile.html')

def update_profile(request):
    current_user = request.user
    user_type  = current_user.user_type
    if request.method == 'POST':
        
        
        if user_type == 'Employer':
            company_name = request.POST.get('company_name')
            address = request.POST.get('address')
        
            employer_data = EmployerModel.objects.get(employer=current_user)
            employer_data.company_name = company_name
            employer_data.address = address
            employer_data.save()
            
        else:
            full_name = request.POST.get('full_name')
            contact_numer = request.POST.get('contact_numer')
            last_education = request.POST.get('last_education')
            skills = request.POST.get('skills')
            
            seeker_data = JobSeekerModel.objects.get(seeker=current_user)
            seeker_data.full_name = full_name
            seeker_data.contact_numer = contact_numer
            seeker_data.last_education = last_education
            seeker_data.skills = skills
            seeker_data.save()
            
        return redirect('profile')
            
    
    return render(request, 'update-profile.html')

#---------------Job----------
def job_list(request):
    current_user = request.user
    user_type = current_user.user_type
    
    if user_type == 'JobSeeker':
        job_data = JobPostModel.objects.all()
    else:
        job_data = JobPostModel.objects.filter(posted_by__employer = current_user)
        
    context = {
        'job_data': job_data
    }
    
    return render(request, 'jobs/job-list.html', context)

def add_job(request):
    current_user = request.user
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')
        
        user = EmployerModel.objects.get(employer = current_user)
        
        JobPostModel.objects.create(
            posted_by = user,
            job_title = job_title,
            description = description,
            skills_required = skills_required,
            salary = salary,
            deadline = deadline,
        )
        return redirect('job_list')
    
    
    return render(request, 'jobs/add-job.html')

def update_job(request, job_id):
    job_data = JobPostModel.objects.get(id = job_id)
    
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')
    
  
        job_data.job_title = job_title
        job_data.description = description
        job_data.skills_required = skills_required
        job_data.salary = salary
        job_data.deadline = deadline

        job_data.save()
        
        return redirect('job_list')
    
    context = {
        'job_data': job_data
    }
    return render(request, 'jobs/update-job.html',context)

def delete_job(request, job_id):
    JobPostModel.objects.get(id = job_id).delete()
    return redirect('job_list')


def applied_job(request, job_id):
    job_data = JobPostModel.objects.get(id = job_id)
    current_user = request.user
    
    application_exists = ApplyJobModel.objects.filter(job = job_data).exists()
    if application_exists:
        messages.warning(request,'Already Applied this job')
        return redirect('job_list')
    
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        user = JobSeekerModel.objects.get(seeker = current_user)
        
        ApplyJobModel.objects.create(
            applied_by = user,
            job = job_data,
            resume = resume,
            status = 'Pending',            
        )
        return redirect('my_application')
    context = {
        'job_data': job_data,
    }
    
    return render(request, 'applied_jobs/apply-job.html',context)

def my_application(request):
    current_user = request.user
    job_data = ApplyJobModel.objects.filter(applied_by__seeker = current_user)
    
    context = {
        'job_data': job_data
    }
    
    return render(request, 'applied_jobs/my-application.html', context)

def applicant_list(request, job_id):
    applicant_data = ApplyJobModel.objects.filter(job = job_id)
    
    context = {
        'applicant_data': applicant_data
    }
    
    return render(request, 'jobs/applicant-list.html',context)

def shortlisted(request, applied_id):
    applied_job = ApplyJobModel.objects.get(id = applied_id)
    applied_job.status = 'Shortlisted'
    applied_job.save()
    return redirect('job_list')
    
def rejected(request, applied_id):
    applied_job = ApplyJobModel.objects.get(id = applied_id)
    applied_job.status = 'Rejected'
    applied_job.save()
    return redirect('job_list')