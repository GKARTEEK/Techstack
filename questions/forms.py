from django import forms
from .models import Question, Category, DifficultyLevel
from languages.models import Language, Topic

# Form for submitting a new question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'language', 'category', 'content', 'code_snippet', 'difficulty', 'topics']
        widgets = {
            'language': forms.Select(attrs={'id': 'id_language'}),
            'topics': forms.Select(attrs={'id': 'id_topics'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default empty queryset for topics
        self.fields['topics'].queryset = Topic.objects.none()

        # Dynamically load topics based on selected language
        if 'language' in self.data:
            try:
                language_id = int(self.data.get('language'))
                self.fields['topics'].queryset = Topic.objects.filter(language_id=language_id)
            except (ValueError, TypeError):
                pass  # fallback to empty queryset
        elif self.instance.pk:
            self.fields['topics'].queryset = self.instance.language.topics.all()

# Form for filtering questions
class QuestionFilterForm(forms.Form):
    DIFFICULTY_CHOICES = [('', 'All Difficulties')] + list(DifficultyLevel.choices)

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
