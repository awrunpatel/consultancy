from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.urls import reverse
from django.middleware.csrf import get_token
from django.views import View
from django.contrib import messages
from userauth.models import User
from .forms import UserForm

class UserListView(View):
    template_name = 'dashboard/users/list.html'

    def get(self, request, *args, **kwargs):
    
        users = User.objects.all().order_by('-id')
        
        return render(request, self.template_name, context={
            'users': users,
        })

class UserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form = UserForm(instance=user)
            title = "Update User"
        else:
            user = None
            form = UserForm()
            title = "Create User"

        return render(request, 'dashboard/users/users.html', context={
            'form': form,
            'title': title,
            'user_id': user_id,
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form = UserForm(request.POST, instance=user)
        else:
            user = None
            form = UserForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:  # Set or update the password only if provided
                user.set_password(password)
            user.save()

            if user_id:
                messages.success(request, "User updated successfully.")
            else:
                messages.success(request, "User created successfully.")
            return redirect('users:user_list')

        title = "Update User" if user_id else "Create User"
        return render(request, 'dashboard/users/users.html', context={
            'form': form,
            'title': title,
            'user_id': user_id,
        })


class UserAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        users = User.objects.all()
        if search_value:
            users = users.filter(
                Q(username__icontains=search_value) | Q(email__icontains=search_value)
            )
        paginator = Paginator(users, length)

        try:
            page_users = paginator.page(page_number)
        except EmptyPage:
            page_users = []

        data = []
        for user in page_users:
            data.append(
                [
                    user.username,
                    user.get_full_name(),
                    user.mobile_number,
                    user.email,
                    user.role,
                    self.get_action(user.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": User.objects.count(),
                "recordsFiltered": users.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, user_id):
        request = self.request  
        csrf_token = get_token(request)
        edit_url = reverse('users:user_edit', kwargs={'pk': user_id})
        delete_url = reverse('generic:delete')  # Adjust to your delete URL pattern
        backurl = reverse('users:user_list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{user_id}" />
                <input type="hidden" name="_selected_type" value="user" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
