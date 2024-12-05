from django import forms
from .models import Blog
from django.utils import timezone
from django.template.defaultfilters import slugify

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'author', 'content', 'image', 'status', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog slug'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter blog content', 'rows': 10}),
            'image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'title': 'Blog Title',
            'slug': 'Slug',
            'author': 'Author',
            'content': 'Content',
            'image': 'Image URL',
            'status': 'Status',
            'published_date': 'Published Date',
        }

    def save(self, commit=True):
        blog = super().save(commit=False)
        if not blog.slug:
            blog.slug = slugify(blog.title)

        if commit:
            blog.save()

        return blog
