from django import forms

from posts.models import Post


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
        Post.objects.create(
            author=user,
            photo=image,
            content=content,
        )
