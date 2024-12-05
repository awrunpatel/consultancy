from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Blog
from .forms import BlogForm
from django.middleware.csrf import get_token
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse



class BlogListView(View):
    template_name = 'dashboard/blogs/list.html'

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all()
        return render(request, self.template_name, {
            'blogs': blogs
        })


class BlogView(View):
    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get('pk')
        if blog_id:
            blog = get_object_or_404(Blog, id=blog_id)
            form = BlogForm(instance=blog)
            title = "Update Blog"
        else:
            form = BlogForm()
            title = "Create Blog"

        return render(request, 'dashboard/blogs/blogs.html', context={
            'form': form,
            'title': title,
            'pk': blog_id
        })

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get('pk')
        if blog_id:
            blog = get_object_or_404(Blog, id=blog_id)
            form = BlogForm(request.POST, instance=blog)
        else:
            form = BlogForm(request.POST)

        if form.is_valid():
            form.save()
            if blog_id:
                messages.success(request, "Blog updated successfully.")
            else:
                messages.success(request, "Blog created successfully.")
            return redirect('blogs:blog_list')

        title = "Update Blog" if blog_id else "Create Blog"
        return render(request, 'dashboard/blogs/blogs.html', context={
            'form': form,
            'title': title,
            'pk': blog_id
        })


class BlogAjaxView(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        blogs = Blog.objects.all().order_by("-created_at")

        if search_value:
            blogs = blogs.filter(title__icontains=search_value)

        paginator = Paginator(blogs, length)

        try:
            page_blogs = paginator.page(page_number)
        except EmptyPage:
            page_blogs = []

        data = []
        for blog in page_blogs:
            data.append(
                [
                    blog.title,
                    blog.author.username,
                    blog.published_date.strftime('%Y-%m-%d') if blog.published_date else "N/A",
                    blog.status.capitalize(),
                    self.get_action(blog.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": Blog.objects.count(),
                "recordsFiltered": blogs.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, blog_id):
        request = self.request
        csrf_token = get_token(request)

        edit_url = reverse('blogs:blog_update', kwargs={'pk': blog_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('blogs:blog_list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{blog_id}" />
                <input type="hidden" name="_selected_type" value="blog" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
