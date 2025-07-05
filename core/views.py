from .models import Job
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from django.shortcuts import redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.contrib import messages
from .models import Job, JobApplication

def home(request):
    query = request.GET.get('q', '')
    job_list = Job.objects.all().order_by('-created_at')

    if query:
        job_list = job_list.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )

    paginator = Paginator(job_list, 2)  # Show 6 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'home.html', {'jobs': jobs, 'query': query})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('home')
    else:
        form = JobForm()
    
    return render(request, 'post_job.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)

    # Check if already applied
    already_applied = JobApplication.objects.filter(applicant=request.user, job=job).exists()
    if already_applied:
        messages.warning(request, "You have already applied for this job.")
    else:
        JobApplication.objects.create(applicant=request.user, job=job)
        messages.success(request, "Application submitted successfully.")

    return redirect('job_detail', job_id=job.id)

@login_required
def job_seeker_dashboard(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    return render(request, 'job_seeker_dashboard.html', {'applications': applications})

