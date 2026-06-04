from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, CompanyRegisterForm, JobForm, ResumeForm, StudentProfileForm
from django.contrib.auth.decorators import login_required
from .models import Student, Company, Job, Application
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            Student.objects.create(
                user=user
            )

            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'student/register.html',
        {'form': form}
    )


@login_required
def dashboard(request):

    return render(
        request,
        'student/dashboard.html'
    )
    
    
@login_required
def profile(request):

    student = Student.objects.get(
        user=request.user
    )

    return render(
        request,
        'student/profile.html',
        {'student': student}
    )
    
    
def company_register(request):

    if request.method == "POST":

        form = CompanyRegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            Company.objects.create(
                user=user,
                company_name=user.username,
                email=user.email,
                location='Unknown',
                description='Company Profile'
            )

            return redirect('login')

    else:
        form = CompanyRegisterForm()

    return render(
        request,
        'company/register.html',
        {'form': form}
    )
    
    
@login_required
def create_job(request):
    print("Current User:", request.user)

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:
        return HttpResponse(
            "Only company accounts can create jobs."
        )

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(
                commit=False
            )

            job.company = company

            job.save()

            return redirect(
                'job_list'
            )

    else:

        form = JobForm()

    return render(
        request,
        'company/create_job.html',
        {'form': form}
    )
    
    
@login_required
def job_list(request):

    jobs = Job.objects.all()

    search = request.GET.get(
        'search'
    )

    if search:

        jobs = jobs.filter(
            title__icontains=search
        )

    context = {
        'jobs': jobs
    }

    return render(
        request,
        'jobs/job_list.html',
        context
    )
    
    
@login_required
def apply_job(request, job_id):

    student = Student.objects.filter(
        user=request.user
    ).first()

    if not student:
        return HttpResponse(
            "Only students can apply."
        )

    job = get_object_or_404(
        Job,
        id=job_id
    )
    
    if student.cgpa < job.minimum_cgpa:

        return HttpResponse(
            f"You are not eligible. "
            f"Required CGPA: {job.minimum_cgpa}"
        )

    already_applied = Application.objects.filter(
        student=student,
        job=job
    ).exists()

    if already_applied:
        return HttpResponse(
            "You already applied."
        )

    Application.objects.create(
        student=student,
        job=job
    )

    return HttpResponse(
        "Application Submitted Successfully."
    )
    
    
@login_required
def my_applications(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    applications = Application.objects.filter(
        student=student
    )

    return render(
        request,
        'student/my_applications.html',
        {
            'applications': applications
        }
    )
    
    
@login_required
def company_applicants(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:
        return HttpResponse(
            "Only companies can access this page."
        )

    applications = Application.objects.filter(
        job__company=company
    )

    return render(
        request,
        'company/applicants.html',
        {
            'applications': applications
        }
    )
    
    
@login_required
def update_status(request, app_id, status):

    application = get_object_or_404(
        Application,
        id=app_id
    )

    application.status = status

    application.save()

    return redirect(
        'company_applicants'
    )
    
    
@login_required
def company_dashboard(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:
        return HttpResponse(
            "Only companies can access."
        )

    jobs = Job.objects.filter(
        company=company
    )

    return render(
        request,
        'company/dashboard.html',
        {
            'jobs': jobs
        }
    )
    
    
@login_required
def upload_resume(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    if not student:
        return HttpResponse(
            "Only students can upload resumes."
        )

    if request.method == 'POST':

        form = ResumeForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()

            return redirect(
                'profile'
            )

    else:

        form = ResumeForm(
            instance=student
        )

    return render(
        request,
        'student/upload_resume.html',
        {
            'form': form
        }
    )
    
    
@login_required
def analytics(request):

    context = {
        'students': Student.objects.count(),
        'companies': Company.objects.count(),
        'jobs': Job.objects.count(),
        'applications': Application.objects.count(),
    }

    return render(
        request,
        'analytics.html',
        context
    )
    
    
@login_required
def edit_profile(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    if not student:
        return HttpResponse(
            "Student profile not found."
        )

    if request.method == 'POST':

        form = StudentProfileForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            return redirect(
                'profile'
            )

    else:

        form = StudentProfileForm(
            instance=student
        )

    return render(
        request,
        'student/edit_profile.html',
        {
            'form': form
        }
    )
    
    
@login_required
def edit_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    form = JobForm(
        request.POST or None,
        instance=job
    )

    if form.is_valid():

        form.save()

        return redirect(
            'company_dashboard'
        )

    return render(
        request,
        'company/edit_job.html',
        {
            'form': form
        }
    )
    
    
@login_required
def delete_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    job.delete()

    return redirect(
        'company_dashboard'
    )
    
    
def custom_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if Company.objects.filter(
                user=user
            ).exists():

                return redirect(
                    'company_dashboard'
                )

            elif Student.objects.filter(
                user=user
            ).exists():

                return redirect(
                    'dashboard'
                )

    return render(
        request,
        'student/login.html'
    )