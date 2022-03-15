from django.forms import ModelForm
from django import forms

from .models import Group, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
    text = forms.CharField(
        label='Текст поста',
        widget=forms.Textarea,
        help_text='Текст нового поста',
        required=True
    )
    group = forms.ModelChoiceField(
        help_text='Группа, к которой будет относиться пост',
        queryset=Group.objects.all(),
        required=False
    )

    def clean_subject(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError(
                'Вы должны обязательно что-то написать'
            )
        return data
