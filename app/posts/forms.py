from django import forms
from django.forms import ModelForm

from posts.models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        # 리스트가 아니라 튜플형태로 적어도 된다()
        fields = ['photo', 'content']


class PostForm(forms.Form):
    image = forms.ImageField(
        label='사진 올리기',
    )
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'style': 'resize: none',
            }
        )
    )

    def post_create(self, user):
        content = self.cleaned_data['content']
        image = self.cleaned_data['image']
        post = Post.objects.create(
            author=user,
            photo=image,
            content=content,
        )
        return post
