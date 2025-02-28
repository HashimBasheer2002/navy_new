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



class MockTest(models.Model):
    SECTION_CHOICES = [
        ('artificer apprentice', 'Artificer Apprentice'),
        ('navy tradesman', 'Navy Tradesman '),
        ('navy chargeman', 'Navy Chargeman '),
        ('indian navy entrance test', 'Indian Navy Entrance Test'),
        ('indian navy angniveer mr', 'Indian Navy Agniveer MR'),
        ('indian navy angniveer ssr', 'Indian Navy Agniveer SSR'),
        ('naval dockyard', 'Naval Dockyard'),
    ]
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mock_tests")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_section_display()


class Question(models.Model):
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=200, null=True)  # Renamed from "Questions" to "text"
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(help_text="1, 2, 3, or 4")

    def __str__(self):
        return self.text  # Now it correctly returns the question text



class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.IntegerField()



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