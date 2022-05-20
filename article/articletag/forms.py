from django import forms
from articletag.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model =User
        fields = "__all__"

class ArticleForm(forms.ModelForm):
    class Meta:
        model =Article
        fields = "__all__"

class TagForm(forms.ModelForm):
    class Meta:
        model =Tag
        fields = "__all__"                
