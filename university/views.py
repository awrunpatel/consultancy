from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from .models import University, UniversityCourse, Intake
from .forms import UniversityForm, UniversityCourseForm, IntakeForm
from django.middleware.csrf import get_token
from django.urls import reverse

class UniversityListView(View):
    template_name = 'dashboard/university/list.html'

    def get(self, request, *args, **kwargs):
        universities = University.objects.all()
        return render(request, self.template_name, {
            'universities': universities
        })

class UniversityView(View):
    def get(self, request, *args, **kwargs):
        university_id = kwargs.get('pk')
        if university_id:
            university = get_object_or_404(University, id=university_id)
            form = UniversityForm(instance=university)
            title = "Update University"
        else:
            form = UniversityForm()
            title = "Create University"
        
        return render(request, 'dashboard/university/university.html', context={
            'form': form,
            'title': title,
            'pk': university_id
        })

    def post(self, request, *args, **kwargs):
        university_id = kwargs.get('pk')
        if university_id:
            university = get_object_or_404(University, id=university_id)
            form = UniversityForm(request.POST, request.FILES, instance=university)
        else:
            form = UniversityForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            if university_id:
                messages.success(request, "University updated successfully.")
            else:
                messages.success(request, "University created successfully.")
            return redirect('universities:university_list')
        
        title = "Update University" if university_id else "Create University"
        return render(request, 'dashboard/university/university.html', context={
            'form': form,
            'title': title,
            'pk': university_id
        })


class UniversityAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        universities = University.objects.all().order_by("name")

        if search_value:
            universities = universities.filter(name__icontains=search_value)

        paginator = Paginator(universities, length)

        try:
            page_universities = paginator.page(page_number)
        except EmptyPage:
            page_universities = []

        data = []
        for university in page_universities:
            data.append(
                [
                    university.name,
                    university.country,
                    university.city,
                    self.get_action(university.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": University.objects.count(),
                "recordsFiltered": universities.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, university_id):
        request = self.request  
        csrf_token = get_token(request)

        edit_url = reverse('universities:update_university', kwargs={'pk': university_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('universities:university_list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{university_id}" />
                <input type="hidden" name="_selected_type" value="university" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
    

class UniversityCourseListView(View):
    template_name = 'dashboard/university/universitycourselist.html'

    def get(self, request, *args, **kwargs):
        universitycourse = UniversityCourse.objects.all()
        return render(request, self.template_name, {
            'universitycourse': universitycourse
        })

class UniversityCourseView(View):
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        if course_id:
            course = get_object_or_404(UniversityCourse, id=course_id)
            form = UniversityCourseForm(instance=course)
            title = "Update University Course"
        else:
            form = UniversityCourseForm()
            title = "Create University Course"
        
        return render(request, 'dashboard/university/course.html', context={
            'form': form,
            'title': title,
            'pk': course_id
        })

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        if course_id:
            course = get_object_or_404(UniversityCourse, id=course_id)
            form = UniversityCourseForm(request.POST, instance=course)
        else:
            form = UniversityCourseForm(request.POST)
        
        if form.is_valid():
            form.save()
            if course_id:
                messages.success(request, "University Course updated successfully.")
            else:
                messages.success(request, "University Course created successfully.")
            return redirect('universities:university_course_list')
        
        title = "Update University Course" if course_id else "Create University Course"
        return render(request, 'dashboard/university/course.html', context={
            'form': form,
            'title': title,
            'pk': course_id
        })

class UniversityCourseAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        # Query the UniversityCourse model
        courses = UniversityCourse.objects.all().order_by("name")

        if search_value:
            # Search filter (adjust based on your model fields)
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
                    course.name,
                    course.university.name,
                    course.level,
                    course.duration_years,
                    course.tuition_fee,
                    self.get_action(course.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": UniversityCourse.objects.count(),
                "recordsFiltered": courses.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, course_id):
        request = self.request
        csrf_token = get_token(request)

        edit_url = reverse('universities:update_university_course', kwargs={'pk': course_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('universities:university_course_list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{course_id}" />
                <input type="hidden" name="_selected_type" value="university_course" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
    
class IntakeListView(View):
    template_name = 'dashboard/university/intakelist.html'

    def get(self, request, *args, **kwargs):
        intake = Intake.objects.all()
        return render(request, self.template_name, {
            'intake': intake
        })

class IntakeView(View):
    def get(self, request, *args, **kwargs):
        intake_id = kwargs.get('pk')
        if intake_id:
            intake = get_object_or_404(Intake, id=intake_id)
            form = IntakeForm(instance=intake)
            title = "Update Intake"
        else:
            form = IntakeForm()
            title = "Create Intake"
        
        return render(request, 'dashboard/university/intake.html', context={
            'form': form,
            'title': title,
            'pk': intake_id
        })

    def post(self, request, *args, **kwargs):
        intake_id = kwargs.get('pk')
        if intake_id:
            intake = get_object_or_404(Intake, id=intake_id)
            form = IntakeForm(request.POST, instance=intake)
        else:
            form = IntakeForm(request.POST)
        
        if form.is_valid():
            form.save()
            if intake_id:
                messages.success(request, "Intake updated successfully.")
            else:
                messages.success(request, "Intake created successfully.")
            return redirect('universities:intake_list')
        
        title = "Update Intake" if intake_id else "Create Intake"
        return render(request, 'dashboard/university/intake.html', context={
            'form': form,
            'title': title,
            'pk': intake_id
        })

class IntakeAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        # Query the Intake model
        intakes = Intake.objects.all().order_by("course__name")

        if search_value:
            # Search filter (adjust based on your model fields)
            intakes = intakes.filter(course__name__icontains=search_value)

        paginator = Paginator(intakes, length)

        try:
            page_intakes = paginator.page(page_number)
        except EmptyPage:
            page_intakes = []

        data = []
        for intake in page_intakes:
            data.append(
                [
                    intake.course.name,
                    intake.intake_month,
                    intake.application_deadline.strftime('%Y-%m-%d') if intake.application_deadline else "N/A",
                    self.get_action(intake.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": Intake.objects.count(),
                "recordsFiltered": intakes.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, intake_id):
        request = self.request
        csrf_token = get_token(request)

        edit_url = reverse('universities:update_intake', kwargs={'pk': intake_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('universities:intake_list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{intake_id}" />
                <input type="hidden" name="_selected_type" value="intake" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''