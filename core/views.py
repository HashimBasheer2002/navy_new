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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
from .models import Membership
from django.conf import settings
@login_required
def home(request):
    role = request.user.groups.first().name if request.user.groups.exists() else 'guest'
    experiences = Experience.objects.all().order_by('-created_at')  # Order by latest shared experience
    return render(request, 'home.html', {'role': role, 'experiences': experiences})

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Membership  # Ensure you import the Membership model

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    amount = 30000  # ₹300 in paise
    order_data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    }
    order = razorpay_client.order.create(data=order_data)
    return JsonResponse(order)


# Payment success handler
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from .models import Membership

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from .models import Membership

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        payment_id = data.get("razorpay_payment_id")
    elif request.method == "GET":
        payment_id = request.GET.get("payment_id")  # Extract from GET request

    if not payment_id:
        return JsonResponse({"error": "Payment ID not provided"}, status=400)

    try:
        # Verify payment
        razorpay_client.payment.fetch(payment_id)

        # Activate membership for the user
        membership, created = Membership.objects.get_or_create(user=request.user)
        membership.is_active = True
        membership.payment_id = payment_id
        membership.save()

        # Redirect to create_course after successful payment
        return redirect("create_course")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def subscribe(request):
    return render(request, "subscribe.html", {"razorpay_key": settings.RAZORPAY_KEY_ID})


# Middleware for access control
from functools import wraps
from django.shortcuts import redirect
from .models import Membership  # Ensure you import Membership

from django.shortcuts import redirect
from functools import wraps
from .models import Membership

def membership_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            membership = Membership.objects.get(user=request.user)
            if not membership.is_active:
                return redirect("subscribe")  # Redirect non-members to the subscription page
        except Membership.DoesNotExist:
            return redirect("subscribe")  # If no membership, redirect to subscribe

        return view_func(request, *args, **kwargs)

    return _wrapped_view




# Protected page




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
@membership_required
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Purchase

from .models import Course, UserCourse


def buy_course(request, course_id):
    if request.user.is_authenticated:
        course = Course.objects.get(id=course_id)

        # Check if the user already owns the course
        if not UserCourse.objects.filter(user=request.user, course=course).exists():
            UserCourse.objects.create(user=request.user, course=course)  # Store who applied

        return redirect('my_courses')  # Redirect to My Courses after purchase

    return redirect('login')  # Redirect to login if not authenticated


def course_applicants(request, course_id):
    course = Course.objects.get(id=course_id)

    # Ensure only the veteran (course creator) can view
    if request.user != course.veteran:
        return redirect('home')

    applicants = UserCourse.objects.filter(course=course)
    return render(request, "course_applicants.html", {"course": course, "applicants": applicants})

@login_required
def my_courses(request):
    purchased_courses = Purchase.objects.filter(user=request.user, payment_status=True).select_related('course')
    courses = [purchase.course for purchase in purchased_courses]

    return render(request, 'my_courses.html', {'courses': courses})


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
 # Ensures only paid members can access
@user_passes_test(is_admin)
def post_job(request):
    if request.method == "POST":
        form = JobOpportunityForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')  # Redirect to job listings
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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VeteranProfile
from .forms import VeteranProfileForm

@login_required
def create_or_update_profile(request):
    # Check if the user already has a profile
    try:
        profile = request.user.veteranprofile
    except VeteranProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        if profile:
            form = VeteranProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = VeteranProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the profile
            profile = form.save(commit=False)
            profile.user = request.user  # Set the user to the current logged-in user
            profile.save()
            return redirect('view_profile')  # Redirect to the profile page after saving
    else:
        form = VeteranProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


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



from .models import StudyMaterial
def study_materials(request):
    materials = StudyMaterial.objects.all().order_by('-added_at')
    return render(request, 'study_meterials.html', {'materials': materials})


from django.shortcuts import render, redirect
from .models import StudyMaterial
from .forms import StudyMaterialForm


def add_study_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('study_materials')  # Redirect to the study materials list page
    else:
        form = StudyMaterialForm()

    return render(request, 'add_study_meterial.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
def admin_required(view_func):
    return user_passes_test(lambda user: user.is_superuser)(view_func)

from django.contrib.auth import get_user_model
User = get_user_model()
@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, "users_list.html", {"users": users})


def list_veterans(request):
    veterans = VeteranProfile.objects.all()  # Fetch all veteran profiles
    return render(request, 'veteran_list.html', {'veterans': veterans})

def view_veteran_profile(request, pk):
    veteran = get_object_or_404(VeteranProfile, pk=pk)  # Fetch the specific veteran profile
    return render(request, 'veteran_profile.html', {'veteran': veteran})