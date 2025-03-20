from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('veteran', 'Veteran'),
        ('aspirant', 'Aspirant'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='aspirant')

    def __str__(self):
        return f"{self.username} ({self.role})"



class VeteranProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rank = models.CharField(max_length=100)
    years_of_service = models.IntegerField()
    achievements = models.TextField()
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class AspirantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    age = models.IntegerField()
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

class Experience(models.Model):
    veteran = models.ForeignKey(VeteranProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    veteran = models.ForeignKey(VeteranProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=100)



from django.db import models
from django.conf import settings

class MockTest(models.Model):
    SECTION_CHOICES = [
        ('artificer apprentice', 'Artificer Apprentice'),
        ('navy tradesman', 'Navy Tradesman'),
        ('navy chargeman', 'Navy Chargeman'),
        ('indian navy entrance test', 'Indian Navy Entrance Test'),
        ('indian navy angniveer mr', 'Indian Navy Agniveer MR'),
        ('indian navy angniveer ssr', 'Indian Navy Agniveer SSR'),
        ('naval dockyard', 'Naval Dockyard'),
    ]
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", default=30)  # Default to 30 minutes
    duration = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mock_tests")

    def __str__(self):
        return f"{self.title} ({self.get_section_display()})"


class MockTestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=True)
    veteran = models.ForeignKey("VeteranProfile", on_delete=models.CASCADE)
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
    improvement_suggestion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.veteran.user.username} - {self.mock_test.title} - Score: {self.score}"



class Question(models.Model):
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=200, null=True)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(help_text="1, 2, 3, or 4")

    def __str__(self):
        return self.text

    def get_option_display(self, option_number=None):
        """Returns the text of the selected option number. Defaults to correct option if no number is provided."""
        options = {
            1: self.option1,
            2: self.option2,
            3: self.option3,
            4: self.option4,
        }
        if option_number is None:
            option_number = self.correct_option  # Default to correct answer
        return options.get(option_number, "Invalid Option")




from django.db import models

class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.IntegerField()
    responses = models.JSONField(default=dict)  # Store selected options as a dictionary
    improvement_suggestion = models.TextField(blank=True, null=True)  # ➡️ Add this line!

    def get_selected_option(self, question_id):
        """Retrieve the selected answer for a specific question."""
        return self.responses.get(str(question_id), "Not Answered")


class QuestionBank(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='question_banks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobOpportunity(models.Model):
    SECTION_CHOICES = [
        ('executive', 'Executive'),
        ('engineering', 'Engineering'),
        ('electrical', 'Electrical'),
        ('education', 'Education'),
        ('medical', 'Medical'),
        ('logistics', 'Logistics'),
        ('submarine', 'Submarine'),
        ('aviation', 'Aviation'),
        ('information_technology', 'Information Technology'),
        ('sports', 'Sports'),
        ('law', 'Law'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(default=True)  # New field for job requirements
    section = models.CharField(max_length=30, choices=SECTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.get_section_display()}"


class JobApplication(models.Model):
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} applied for {self.job.title}"



class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class WallOfHonor(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

MEDIA_TYPE_CHOICES = [
    ('photo', 'Photo'),
    ('video', 'Video'),
]

class WallMedia(models.Model):
    wall_entry = models.ForeignKey(WallOfHonor, on_delete=models.CASCADE, related_name="media")
    media_file = models.FileField(upload_to='wall_media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return f"{self.wall_entry.title} - {self.media_type}"


from django.db import models

from django.db import models

from django.db import models

class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='study_materials/')
    purchase_link = models.URLField(blank=True, null=True)  # External purchase option
    added_at = models.DateTimeField(auto_now_add=True)
    is_special = models.BooleanField(default=False)  # Special book flag
    pdf_file = models.FileField(upload_to='study_materials/pdfs/', blank=True, null=True)  # PDF file

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price field
    is_purchased = models.BooleanField(default=False)  # Purchase tracking

    def __str__(self):
        return self.title


class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)  # Track payment success
    purchased_at = models.DateTimeField(auto_now_add=True)

class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Student who applied
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} applied for {self.course.title}"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, unique=True,default=True)  # Ensure this exists
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)


class PurchasedMaterial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Participation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'user')  # Prevent duplicate participation

    def __str__(self):
        return f"{self.user.username} - {self.campaign.title}"