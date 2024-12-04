from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from students.forms import StudentAddForm, StudentEditForm
from userauth.forms import *
from userauth.models import *
from students.models import *
from dashboard.models import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from students.forms import StudentForm
from django.http import JsonResponse
from django.urls import reverse
from django.middleware.csrf import get_token

class StudentView(View):
    template_name = 'dashboard/students/add.html'

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudentAddForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student added/updated successfully")
                return redirect('students:list')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {'form': form})

    def handle_errors(self, form):
        # Print errors for each sub-form
        form_instances = {
            'user_form': form.user_form,
            'permanent_address_form': form.permanent_address_form,
            'temporary_address_form': form.temporary_address_form,
            'payment_address_form': form.payment_address_form,
            'personal_info_form': form.personal_info_form,
            'student_form': form.student_form,
            'emergency_contact_form': form.emergency_contact_form,
            'emergency_address_form': form.emergency_address_form,
        }

        for form_name, form_instance in form_instances.items():
            print(f"{form_name} is valid: {form_instance.is_valid()}")
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class StudentEditView(View):
    template_name = 'dashboard/students/edit.html'

    def get(self, request, *args, **kwargs):
        student_id = kwargs.pop('id', None)
        student = get_object_or_404(Students, id=student_id)
        personalinfo = get_or_none(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()

        form = StudentEditForm(instance=student, personalinfo_instance=personalinfo)
        return render(request, self.template_name, {
            'form': form,
            'student_id': student_id,
            'education_history_form': education_history_form,
        })
    def post(self, request, *args, **kwargs):
        student_id = kwargs.pop('id', None)
        student = get_object_or_404(Students, id=student_id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()
        
        form = StudentEditForm(data=request.POST, instance=student,
                               personalinfo_instance=personalinfo)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully")
            return redirect('students:list')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name,
                      {'form': form, 'student_id': student_id, 'education_history_form': education_history_form,
                       })
    
class StudentList(View):
    template_name = 'dashboard/students/list.html'

    def get(self, request, *args, **kwargs):
        students = Students.objects.all().order_by("-id")
        context = {
            "students": students
        }
        return render(request, self.template_name, context)


class StudentAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        students = Students.objects.all().order_by("-id")

        if search_value:
            students = students.filter(
                Q(user__first_name__icontains=search_value) |
                Q(user__last_name__icontains=search_value) |
                Q(student_id__icontains=search_value)
            )

        paginator = Paginator(students, length)
        page_students = paginator.page(page_number)

        data = []
        for student in page_students:
            data.append([
                self.get_checkbox_html(student.id),
                student.user.get_full_name(),
                student.user.email,
                str(student.course_name) if student.course_name else "",
                self.get_action(student)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)
    
    def get_checkbox_html(self, student_id):
        return f'''
            <div class="form-check">
                <label for="checkbox_{student_id}_question"></label>
                <input class="form-check-input" type="checkbox" 
                       name="_selected_id" value="{student_id}" 
                       id="checkbox_{student_id}_question">
            </div>
        '''
    def get_action(self, student):
        request = self.request  
        csrf_token = get_token(request)
        student_id = student.id
        edit_url = reverse('students:edit', kwargs={'id': student_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('students:list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{student_id}" />
                <input type="hidden" name="_selected_type" value="student" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
class EducationalHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        # Fetch student based on pk
        student = Students.objects.filter(id=kwargs.get("pk")).first()
        educations_history = EducationHistory.objects.filter(user=student.user).order_by('-id')

        # Apply search if search_value is present
        if search_value:
            educations_history = educations_history.filter(
                Q(degree_name__icontains=search_value) |
                Q(institution_name__icontains=search_value) |
                Q(graduation_year__icontains=search_value) |
                Q(major_subject__icontains=search_value)
            )

        # Paginator setup
        paginator = Paginator(educations_history, length)

        try:
            educations_history_page = paginator.page(page_number)
        except EmptyPage:
            educations_history_page = paginator.page(paginator.num_pages)

        # Prepare data for response
        data = []
        for history in educations_history_page:
            data.append([
                history.degree_name,
                history.institution_name,
                history.graduation_year,
                history.major_subject,
                self.get_action(student.id, history.id, history.file)
            ])

        # Return JSON response
        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, student_id, obj_id, file):
        request = self.request  
        csrf_token = get_token(request)
        delete_url = reverse('generic:delete')
        backurl = reverse('students:edit', kwargs={'id': student_id})

        view_file = ""
        if file and file != "None":
            view_file = f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                {view_file}
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="educational_history" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
    def post(self, request, *args, **kwargs):
        form = EducationHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            education_history = form.save(commit=False)
            student = Students.objects.filter(id=self.kwargs['pk']).first()  # Use 'pk' instead of 'id'
            education_history.user = student.user
            education_history.save()

            messages.success(request, "Educational history added successfully!")

            return redirect(reverse('students:edit', kwargs={'id': self.kwargs['pk']}))

        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)