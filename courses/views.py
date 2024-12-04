from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.urls import reverse
from .models import Courses
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import get_token
from .forms import CourseForm

class CourseListView(View):
    template_name = 'dashboard/courses/list.html'

    def get(self, request, *args, **kwargs):
        courses = Courses.objects.all()  
        return render(request, self.template_name, {
            'courses': courses  
        })

class CourseView(View):
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        if course_id:
            course = get_object_or_404(Courses, id=course_id)
            form = CourseForm(instance=course)
            title = "Update Course"
        else:
            form = CourseForm()
            title = "Create Course"
        
        return render(request, 'dashboard/courses/courses.html', context={
            'form': form,
            'title': title,
            'pk': course_id  # Add course_id to the context
        })

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        if course_id:
            course = get_object_or_404(Courses, id=course_id)
            form = CourseForm(request.POST, instance=course)
        else:
            form = CourseForm(request.POST)
        
        if form.is_valid():
            form.save()
            if course_id:
                messages.success(request, "Course updated successfully.")
            else:
                messages.success(request, "Course created successfully.")
            return redirect('courses:course_list')
        
        title = "Update Course" if course_id else "Create Course"
        return render(request, 'dashboard/courses/courses.html', context={
            'form': form,
            'title': title,
            'pk': course_id  # Pass course_id to the context
        })

class CourseAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        # Properly query the Courses model
        courses = Courses.objects.all().order_by("course_name")

        if search_value:
            # Adjust this filter to match your model fields and search logic
            courses = courses.filter(name__icontains=search_value)

        paginator = Paginator(courses, length)

        try:
            page_courses = paginator.page(page_number)
        except EmptyPage:
            page_courses = []

        data = []
        for course in page_courses:
            data.append(
                [
                    course.course_name,
                    course.fee,
                    course.duration_in_weeks,
                    course.start_date.strftime('%Y-%m-%d') if course.start_date else "N/A",
                    course.end_date.strftime('%Y-%m-%d') if course.end_date else "N/A",
                    "Active" if course.is_active else "Inactive",
                    self.get_action(course.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": Courses.objects.count(),
                "recordsFiltered": courses.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, course_id):
        request = self.request  # Assuming `self.request` is available in your view.
        csrf_token = get_token(request)

        edit_url = reverse('courses:update_course', kwargs={'pk': course_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('courses:course_list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{course_id}" />
                <input type="hidden" name="_selected_type" value="course" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
