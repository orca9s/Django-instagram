from django import forms


class PostForm(forms.Form):
    image = forms.ImageField()
    content = forms.CharField(max_length=50)
