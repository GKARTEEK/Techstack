from django import forms
from .models import Question, Category, DifficultyLevel  # Import DifficultyLevel
from languages.models import Language, Topic

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'code_snippet', 'difficulty', 'language', 'topics', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'code_snippet': forms.Textarea(attrs={'rows': 8, 'class': 'font-mono'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topics'].queryset = Topic.objects.none()
        
        if 'language' in self.data:
            try:
                language_id = int(self.data.get('language'))
                self.fields['topics'].queryset = Topic.objects.filter(language_id=language_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['topics'].queryset = self.instance.language.topics.all()

class QuestionFilterForm(forms.Form):
    from .models import DifficultyLevel  # Import DifficultyLevel inside the class if needed

    DIFFICULTY_CHOICES = [('', 'All Difficulties')] + list(DifficultyLevel.choices)  # Fix here

    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        required=False
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        empty_label="All Languages",
        required=False
    )
