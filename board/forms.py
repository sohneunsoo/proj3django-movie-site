from django import forms
from .models import StarComments
class StarCommentsForm(forms.ModelForm):
    class Meta:
        model = StarComments
        fields = ["starscore","content", "moviecode"]
        choicelist = []
        for i in range(1,11):
            choicelist.append((str(i),i))
        widgets = {
            'moviecode': forms.HiddenInput(),
            'starscore': forms.RadioSelect(attrs={'class': 'form-check-inline'
                },choices=choicelist),
            'content': forms.TextInput(
                attrs={
                    'placeholder': '영화에 관련된 댓글을 적어주세요',
                    'class': 'form-control',
                'rows': 3
                }
            )
        }