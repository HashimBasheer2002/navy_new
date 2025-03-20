from django import forms
from .models import CustomUser
from .models import VeteranProfile,News,AspirantProfile
from .models import MockTest, Question, UserResponse,JobOpportunity, JobApplication
from .models import WallOfHonor, WallMedia


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        # Filter role choices to exclude 'admin'
        filtered_choices = [choice for choice in CustomUser.ROLE_CHOICES if choice[0] != 'admin']
        self.fields['role'].choices = filtered_choices



class VeteranProfileForm(forms.ModelForm):
    class Meta:
        model = VeteranProfile
        fields = ['rank', 'years_of_service', 'achievements', 'bio', 'profile_photo']

class AspirantProfileForm(forms.ModelForm):
    model=AspirantProfile
    fields= ['email','age','bio','profile_photo']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter news title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter news description'}),
        }


class MockTestForm(forms.ModelForm):
    duration = forms.IntegerField(min_value=1, help_text="Duration in minutes")

    class Meta:
        model = MockTest
        fields = ['section', 'duration']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_option']

class TestSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super(TestSubmissionForm, self).__init__(*args, **kwargs)

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=[
                    (1, question.option1),
                    (2, question.option2),
                    (3, question.option3),
                    (4, question.option4)
                ],
                widget=forms.RadioSelect,
                required=True
            )




class JobOpportunityForm(forms.ModelForm):
    class Meta:
        model = JobOpportunity
        fields = ['title', 'description', 'requirements', 'section']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job','resume']





class WallOfHonorForm(forms.ModelForm):
    class Meta:
        model = WallOfHonor
        fields = ['title', 'description']

class WallMediaForm(forms.ModelForm):
    class Meta:
        model = WallMedia
        fields = ['media_file', 'media_type']


from django import forms
from .models import StudyMaterial

from django import forms
from .models import StudyMaterial

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'image', 'price', 'pdf_file']  # Include PDF field





from django import forms
from .models import QuestionBank

class QuestionBankForm(forms.ModelForm):
    class Meta:
        model = QuestionBank
        fields = ['title', 'pdf']
