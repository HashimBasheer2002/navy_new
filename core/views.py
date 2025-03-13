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

def about(request):
    return render(request,'about.html')



def index(request):
    return render(request,'index.html')

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

    profile, created = VeteranProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = VeteranProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = VeteranProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})






def memebership(request):
    return render(request,'membership.html')


from django.utils.timezone import now

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

    return render(request, 'create_mock_test.html', {'form': form, 'current_time': now()})


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
@login_required
def mock_test_list(request):
    tests = MockTest.objects.all()

    # Fetch the latest 5 admin suggestions (excluding empty ones)
    recent_suggestions = MockTestResult.objects.exclude(improvement_suggestion__isnull=True).exclude(improvement_suggestion="").order_by('-date_taken')[:5]

    return render(request, 'mock_test_list.html', {
        'tests': tests,
        'recent_suggestions': recent_suggestions  # Pass suggestions to template
    })


#attempting test

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import MockTest, Question, UserResponse
from .forms import TestSubmissionForm

from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MockTest, UserResponse
from .forms import TestSubmissionForm

from django.shortcuts import redirect
from django.utils.timezone import now

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import MockTest, UserResponse, MockTestResult, VeteranProfile
from .forms import TestSubmissionForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MockTest, UserResponse, MockTestResult, VeteranProfile

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MockTest, UserResponse, MockTestResult, VeteranProfile

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import MockTest, UserResponse, MockTestResult, VeteranProfile

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import MockTest, UserResponse, MockTestResult, VeteranProfile

import json

@login_required
def take_test(request, test_id):
    mock_test = get_object_or_404(MockTest, id=test_id)
    questions = mock_test.questions.all().order_by('id')
    time_limit = mock_test.duration * 60

    if request.method == "POST":
        form = TestSubmissionForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            responses = {}

            for question in questions:
                selected_option = request.POST.get(f'question_{question.id}')
                responses[str(question.id)] = int(selected_option) if selected_option else "Not Answered"

                if selected_option and int(selected_option) == question.correct_option:
                    score += 1

            with transaction.atomic():
                user_response = UserResponse.objects.create(
                    user=request.user, test=mock_test, score=score, responses=json.dumps(responses)
                )

                try:
                    veteran_profile = VeteranProfile.objects.get(user=request.user)
                    MockTestResult.objects.create(
                        veteran=veteran_profile,
                        mock_test=mock_test,
                        score=score
                    )
                except VeteranProfile.DoesNotExist:
                    pass

            return redirect('test_result', test_id=test_id)

    else:
        form = TestSubmissionForm(questions=questions)

    return render(request, 'take_test.html', {
        'mock_test': mock_test,
        'form': form,
        'questions': questions,
        'time_limit': time_limit
    })


@login_required
def test_result(request, test_id):
    """Displays the results of a mock test taken by the user."""
    mock_test = get_object_or_404(MockTest, id=test_id)
    questions = mock_test.questions.all()

    # Get the latest user response for this test
    user_response = UserResponse.objects.filter(user=request.user, test=mock_test).order_by('-id').first()

    selected_answers = {}
    if user_response:
        responses_dict = json.loads(user_response.responses)  # ✅ Convert string back to dictionary
        for q_id, answer in responses_dict.items():  # Now, responses_dict is a valid dictionary
            question = questions.filter(id=int(q_id)).first()
            if question:
                selected_answers[int(q_id)] = (
                    question.get_option_display(int(answer))
                    if answer != "Not Answered"
                    else "Not Answered"
                )

    return render(request, "test_result.html", {
        "mock_test": mock_test,
        "questions": questions,
        "selected_answers": selected_answers,
        "score": user_response.score if user_response else 0,
    })



@login_required
def mock_test_results(request):
    if not request.user.is_staff:  # Ensure only admin users can access
        return HttpResponseForbidden("You are not authorized to view this page.")

    results = MockTestResult.objects.all().order_by('-date_taken')

    return render(request, 'view_test_results.html', {'results': results})




from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseForbidden
from core.models import MockTestResult

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import MockTestResult


@login_required
def suggest_improvement(request, result_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to do this.")

    result = get_object_or_404(MockTestResult, id=result_id)

    if request.method == "POST":
        suggestion = request.POST.get("improvement")
        result.improvement_suggestion = suggestion
        result.save()

    # Redirect to a page where the aspirant can see only their own suggestions
    return redirect(reverse('user_suggestions'))


def is_admin(user):
    return user.is_superuser  # ✅ Corrected



@login_required
@user_passes_test(is_admin)  # Ensures only superusers can access
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
            application.applicant = request.user  # Automatically assign the logged-in user
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
    materials = StudyMaterial.objects.filter(is_special=False).order_by('-added_at')
    special_book = StudyMaterial.objects.filter(is_special=True).first()  # Only one special book

    return render(request, 'study_meterials.html', {
        'materials': materials,
        'special_book': special_book
    })


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import StudyMaterial
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def razorpay_payment(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    order_amount = 50000  # Set price in paise (e.g., ₹500 = 50000 paise)
    order_currency = 'INR'
    order_receipt = f'order_rcptid_{material.id}'

    order = razorpay_client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "receipt": order_receipt,
        "payment_capture": "1"
    })

    return render(request, 'payment_page.html', {
        'material': material,
        'order_id': order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

@csrf_exempt
def payment_success(request):
    return render(request, 'download.html')


from django.http import FileResponse





from django.shortcuts import render, redirect
from .models import StudyMaterial
from .forms import StudyMaterialForm


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import StudyMaterialForm

def add_study_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)  # Handle files
        if form.is_valid():
            form.save()
            messages.success(request, "Study material added successfully!")
            return redirect(reverse('study_materials'))  # Redirect after success
        else:
            messages.error(request, "Error adding the study material. Please check the form.")
    else:
        form = StudyMaterialForm()

    return render(request, 'add_study_meterial.html', {'form': form})




import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from core.models import StudyMaterial ,Payment # Import Payment model if you track payments

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import StudyMaterial, Payment

# Initialize Razorpay client (Ensure this is correctly configured)
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def razorpay_payment(request, material_id):
    study_material = get_object_or_404(StudyMaterial, id=material_id)

    # Ensure the price is valid (minimum 1 INR)
    if study_material.price is None or study_material.price < 1:
        return HttpResponse("Error: Invalid price. The amount must be at least ₹1.00", status=400)

    # Convert price to paise (Razorpay uses paise)
    amount = int(study_material.price * 100)

    # Check if the user has already purchased this material
    if request.user.is_authenticated:
        existing_payment = Payment.objects.filter(user=request.user, study_material=study_material, status="SUCCESS").exists()
        if existing_payment:
            return redirect(study_material.pdf_file.url)  # Redirect to download if already purchased

    # Create Razorpay order
    try:
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "user_email": request.user.email if request.user.is_authenticated else "guest",
                "study_material": study_material.title
            }
        }
        order = razorpay_client.order.create(order_data)
    except razorpay.errors.BadRequestError as e:
        return HttpResponse(f"Error creating Razorpay order: {str(e)}", status=400)

    # Render payment page with order details
    context = {
        "study_material": study_material,
        "order_id": order["id"],
        "amount": amount / 100,  # Convert back to INR for display
        "key": settings.RAZORPAY_KEY_ID,
        "material_id": material_id  # ✅ Ensure this is correctly passed
    }
    return render(request, "razorpay_payment.html", context)






razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_payment(request, material_id):
    study_material = get_object_or_404(StudyMaterial, id=material_id)

    if study_material.is_purchased:
        return JsonResponse({"error": "Already Purchased"}, status=400)

    amount = int(study_material.price * 100)  # Convert to paise
    order_data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    }

    order = razorpay_client.order.create(order_data)

    return JsonResponse({
        "order_id": order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID,
        "material_id": study_material.id
    })


from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import StudyMaterial, Payment


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import StudyMaterial, Payment

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import StudyMaterial, PurchasedMaterial


@login_required
def payment_success(request, material_id):
    try:
        material = StudyMaterial.objects.get(id=material_id)

        # Check if user already has this book
        if not PurchasedMaterial.objects.filter(user=request.user, material=material).exists():
            PurchasedMaterial.objects.create(user=request.user, material=material)
            return JsonResponse({'message': 'Purchase recorded successfully'})
        else:
            return JsonResponse({'message': 'Book already purchased'})

    except StudyMaterial.DoesNotExist:
        return JsonResponse({'error': 'Material not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from django.shortcuts import get_object_or_404
from django.http import FileResponse
from core.models import Payment

from django.shortcuts import get_object_or_404
from django.http import FileResponse
from core.models import Payment

from django.shortcuts import render
from .models import PurchasedMaterial


def my_books(request):
    if not request.user.is_authenticated:
        return redirect('login')

    purchased_books = PurchasedMaterial.objects.filter(user=request.user).select_related('material')

    return render(request, 'my_books.html', {'purchased_books': purchased_books})




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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Campaign, Participation
from django.contrib import messages


# Check if user is admin
def is_admin(user):
    return user.is_superuser


# View all campaigns
@login_required
def view_campaigns(request):
    campaigns = Campaign.objects.all()
    participated_campaigns = Participation.objects.filter(user=request.user).values_list("campaign_id", flat=True)
    return render(request, "view_campaigns.html",
                  {"campaigns": campaigns, "participated_campaigns": participated_campaigns})


# Mark as participate
@login_required
def participate_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    Participation.objects.get_or_create(user=request.user, campaign=campaign)
    messages.success(request, "You have successfully participated in the campaign!")
    return redirect("view_campaigns")


# Admin - Add campaign
@user_passes_test(is_admin)
def add_campaign(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        date = request.POST["date"]
        Campaign.objects.create(title=title, description=description, date=date)
        messages.success(request, "Campaign added successfully!")
        return redirect("admin_campaigns")

    return render(request, "add_campaign.html")


# Admin - Edit campaign
@user_passes_test(is_admin)
def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if request.method == "POST":
        campaign.title = request.POST["title"]
        campaign.description = request.POST["description"]
        campaign.date = request.POST["date"]
        campaign.save()
        messages.success(request, "Campaign updated successfully!")
        return redirect("admin_campaigns")

    return render(request, "edit_campaign.html", {"campaign": campaign})


# Admin - Delete campaign
@user_passes_test(is_admin)
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    campaign.delete()
    messages.success(request, "Campaign deleted successfully!")
    return redirect("admin_campaigns")


# Admin - View participants
@user_passes_test(is_admin)
def view_participants(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    participants = Participation.objects.filter(campaign=campaign)
    return render(request, "view_participants.html", {"campaign": campaign, "participants": participants})
