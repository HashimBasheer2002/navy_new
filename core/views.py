from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserForm,NewsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import  get_object_or_404
from .models import VeteranProfile
from .forms import VeteranProfileForm,AspirantProfileForm
from .models import Course,Experience,News
from .models import MockTest, Question, UserResponse
from .forms import MockTestForm, QuestionForm, TestSubmissionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import JobOpportunity, JobApplication,News
from .forms import JobOpportunityForm, JobApplicationForm
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import WallOfHonor, WallMedia
from .forms import WallOfHonorForm, WallMediaForm
@login_required
def home(request):
    role = request.user.groups.first().name if request.user.groups.exists() else 'guest'
    experiences = Experience.objects.all().order_by('-created_at')  # Order by latest shared experience
    return render(request, 'home.html', {'role': role, 'experiences': experiences})


def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = CustomUserForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def role_based_redirect(request):
    user_role = request.user.role

    if user_role == 'admin':
        return redirect('admin_dashboard')
    elif user_role == 'veteran':
        return redirect('veteran_dashboard')
    else:
        return redirect('aspirant_dashboard')


@login_required
def create_or_update_profile(request):
    try:
        profile = request.user.veteranprofile
    except VeteranProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = VeteranProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            veteran_profile = form.save(commit=False)
            veteran_profile.user = request.user
            veteran_profile.save()
            return redirect('home')
    else:
        form = VeteranProfileForm(instance=profile)

    return render(request, 'profile_form.html', {'form': form})





@login_required
def share_experience(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        veteran_profile = request.user.veteranprofile
        Experience.objects.create(veteran=veteran_profile, title=title, content=content)
        return redirect('home')

    return render(request, 'share_experience.html')

@login_required
def view_experience(request):
    experience = Experience.objects.all()


@login_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        fee = request.POST['fee']
        duration = request.POST['duration']
        veteran_profile = request.user.veteranprofile
        Course.objects.create(
            veteran=veteran_profile,
            title=title,
            description=description,
            fee=fee,
            duration=duration
        )
        return redirect('home')

    return render(request, 'create_course.html')

@login_required()
def view_course(request):
    course = Course.objects.all()
    return render(request,'course.html',{'course':course})


@login_required
def view_profile(request):
    profile = request.user.veteranprofile
    experiences = Experience.objects.filter(veteran=profile).order_by('-created_at')
    return render(request, 'view_profile.html', {'profile': profile, 'experiences': experiences})

@login_required
def edit_profile(request):
    """Allow veterans to create or update their profile."""
    try:
        profile = VeteranProfile.objects.get(user=request.user)
    except VeteranProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = VeteranProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            veteran_profile = form.save(commit=False)
            veteran_profile.user = request.user
            veteran_profile.save()
            return redirect('view_profile')
    else:
        # Always initialize the form, even if no profile exists
        form = VeteranProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})






def memebership(request):
    return render(request,'membership.html')


@login_required
def create_mock_test(request):
    if request.method == "POST":
        form = MockTestForm(request.POST)
        if form.is_valid():
            mock_test = form.save(commit=False)
            mock_test.created_by = request.user
            mock_test.save()
            return redirect('add_question', test_id=mock_test.id)
    else:
        form = MockTestForm()
    return render(request, 'create_mock_test.html', {'form': form})


def delete_test(request):
    test=get_object_or_404(MockTest)
    test.delete()
    return render(request,'mock_test_list')



#veterans adding question

@login_required
def add_question(request, test_id):
    mock_test = get_object_or_404(MockTest, id=test_id)

    if request.method == "POST":
        if "finish" in request.POST:
            return redirect('mock_test_list')

        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.mock_test = mock_test
            question.save()
            return redirect('add_question', test_id=test_id)

    else:
        form = QuestionForm()

    return render(request, 'add_question.html', {'form': form, 'mock_test': mock_test})



#view test
def mock_test_list(request):
    tests = MockTest.objects.all()
    return render(request, 'mock_test_list.html', {'tests': tests})


#attempting test

@login_required
def take_test(request, test_id):
    mock_test = get_object_or_404(MockTest, id=test_id)
    questions = mock_test.questions.all().order_by('id')  # Ensure correct ordering

    if request.method == "POST":
        form = TestSubmissionForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                selected_option = int(form.cleaned_data.get(f'question_{question.id}', 0))
                if selected_option == question.correct_option:
                    score += 1

            UserResponse.objects.create(user=request.user, test=mock_test, score=score)
            return redirect('test_result', test_id=test_id)

    else:
        form = TestSubmissionForm(questions=questions)

    return render(request, 'take_test.html', {'mock_test': mock_test, 'form': form, 'questions': questions})


#test result

@login_required
def test_result(request, test_id):
    test = get_object_or_404(MockTest, id=test_id)
    result = UserResponse.objects.filter(user=request.user, test=test).last()
    return render(request, 'test_result.html', {'test': test, 'result': result})




def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def post_job(request):
    if request.method == "POST":
        form = JobOpportunityForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobOpportunityForm()
    return render(request, 'post_job.html', {'form': form})


def job_list(request):
    jobs = JobOpportunity.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})



@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobOpportunity, id=job_id)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})


def applications(request):
    applications = JobApplication.objects.all()
    return render(request, 'applications.html', {'applications': applications})



def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.save()
            return redirect('news_list')  # Redirect to news list
    else:
        form = NewsForm()
    return render(request, 'post_news.html', {'form': form})

def view_news(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'News.html', {'news': news})



@login_required
def aspirant_profile(request):
    try:
        profile = request.user.aspirantprofile
    except AspirantsProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = AspirantProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            aspirant_profile = form.save(commit=False)
            aspirant_profile.user = request.user
            aspirant_profile.save()
            return redirect('home')
    else:
        form = AspirantProfileForm(instance=profile)

    return render(request, 'aspirant_profile.html', {'form': form})

@login_required
def view_aspirant_profile(request):
    profile = request.user.aspirantprofile
    experiences = Experience.objects.filter(aspirant=profile).order_by('-created_at')
    return render(request, 'view_aspirant_profile.html', {'profile': profile})




# Check if user is admin (or you can use is_superuser or a specific permission)
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def post_wall_entry(request):
    if request.method == "POST":
        form = WallOfHonorForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user
            entry.save()
            # Redirect to add media for this entry, or to the wall list
            return redirect('add_wall_media', entry_id=entry.id)
    else:
        form = WallOfHonorForm()
    return render(request, 'post_wall_entry.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def add_wall_media(request, entry_id):
    entry = get_object_or_404(WallOfHonor, id=entry_id)
    if request.method == "POST":
        form = WallMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.wall_entry = entry
            media.save()
            # Optionally, allow adding more media or finish.
            if "finish" in request.POST:
                return redirect('wall_of_honor')
            else:
                return redirect('add_wall_media', entry_id=entry.id)
    else:
        form = WallMediaForm()
    return render(request, 'add_wall_media.html', {'form': form, 'entry': entry})

@login_required
def wall_of_honor(request):
    # Everyone can view the tributes
    entries = WallOfHonor.objects.all().order_by('-created_at')
    return render(request, 'wall_of_honor.html', {'entries': entries})
