from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .models import *
from courses.models import *
from students.models import *
from userauth.models import *
from events.models import *
from blogs.models import *
from django.db.models import Prefetch, Count
from .forms import *
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.db.models import Q
from django.middleware.csrf import get_token


class DashboardView(View):
    def calculate_user_changes(self, role):
        try:
            one_week_ago = datetime.now() - timedelta(weeks=1)
            new_users_count = User.objects.filter(date_joined__gte=one_week_ago, role=role).count()
            old_users_count = User.objects.filter(date_joined__lt=one_week_ago, role=role).count()
            total_users_count = new_users_count + old_users_count

            if total_users_count == 0:
                change_in_users_percent = 0
            else:
                change_in_users_percent = ((new_users_count - old_users_count) / total_users_count) * 100
            change_in_users_percent = round(change_in_users_percent, 1)

            user_changes = {
                "total": total_users_count,
                "new": new_users_count,
                "old": old_users_count,
                "change": change_in_users_percent
            }
            return user_changes
        except Exception:
            return {
                "total": 0,
                "new": 0,
                "old": 0,
                "change": 0
            }

    def calculate_courses_changes(self):
        try:
            one_week_ago = datetime.now() - timedelta(weeks=1)
            new_courses_count = Courses.objects.filter(start_date__gte=one_week_ago).count()
            old_courses_count = Courses.objects.filter(start_date__lt=one_week_ago).count()

            total_courses_count = new_courses_count + old_courses_count

            if total_courses_count == 0:
                change_in_courses_percent = 0
            else:
                change_in_courses_percent = ((new_courses_count - old_courses_count) / total_courses_count) * 100
            change_in_courses_percent = round(change_in_courses_percent, 1)

            user_changes = {
                "total": total_courses_count,
                "new": new_courses_count,
                "old": old_courses_count,
                "change": change_in_courses_percent
            }
            return user_changes
        except Exception:
            return {
                "total": 0,
                "new": 0,
                "old": 0,
                "change": 0
            }

    def get(self, request, *args, **kwargs):
        students = self.calculate_user_changes("student")
        # teachers = self.calculate_user_changes("teacher")
        courses = self.calculate_courses_changes()
        enquiries = Enquiry.objects.count()
        return render(request, 'dashboard/index.html', context={
            "students": students,
            # "teachers": teachers,
            "courses": courses,
            "enquiries": enquiries
        })

class EnquiryView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/enquiry/list.html')


class EnquiryAjaxView(View):
    def get_action(self, post: Enquiry):
        request = self.request  
        csrf_token = get_token(request)
        delete_url = reverse('generic:delete')
        backurl = reverse('dashboard:enquiry')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <button type="button" class="btn btn-warning btn-sm viewEnquiry">View</button>
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <textarea class="d-none">{post.message}</textarea>
                <input class="d-none phone_number" value="{post.phone_number}" />
                <input class="d-none country" value="{post.get_country_display()}" />

                <input type="hidden" name="_selected_id" value="{post.id}" />
                <input type="hidden" name="_selected_type" value="enquiry" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', None)
        page_number = (start // length) + 1

        posts = Enquiry.objects.filter()
        if search_value:
            posts = posts.filter(Q(email__icontains=search_value) | Q(name__icontains=search_value))
        posts = posts.order_by('-id')

        paginator = Paginator(posts, length)
        page_posts = paginator.page(page_number)
        data = []
        for post in page_posts:
            data.append([
                post.subject,
                post.name,
                post.email,
                post.get_date(),
                self.get_action(post)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data
        }, status=200)
    
class FileManagerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/filemanager.html')

class SettingsView(View):
    def get(self, request, *args, **kwargs):
        settings = SiteSettings.objects.first()
        form = SiteSettingsForm(instance=settings)
        return render(request, 'dashboard/setting.html', {'form': form})

    def post(self, request, *args, **kwargs):
        settings = SiteSettings.objects.first()
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard:settings')  # Make sure 'settings_view' is the correct URL name
        return render(request, 'dashboard/setting.html', {'form': form})
    
class DeleteHelper:
    def get_objects(self, ids, model, type_title, reverse_name=None, title_generator=None, kwargs_generator=None):
        objects = []
        objects_org = []
        try:
            for obj_id in ids:
                try:
                    obj = model.objects.get(id=obj_id)
                    title = title_generator(obj) if title_generator else obj.id
                    url = reverse(reverse_name, kwargs=kwargs_generator(obj)) if reverse_name else "#"

                    objects_org.append(obj)
                    objects.append({
                        "id": obj.id,
                        "type": type_title,
                        "title": title,
                        "url": url
                    })
                except model.DoesNotExist:
                    pass
        except Exception as e:
            print(e)
            pass
        return objects, objects_org
    def get_user(self, ids):
        def user_email(obj):
            return obj.email

        def user_kwargs(obj):
            return {'id': obj.id, 'username': obj.username}  

        return self.get_objects(ids, User, "User", None, user_email, user_kwargs)
    
    def get_educational_history(self, ids):
        def degree_name(obj):
            return obj.degree_name

        def degree_kwargs(obj):
            return {
                'institution_name': obj.institution_name,
                'graduation_year': obj.graduation_year,
                'major_subject': obj.major_subject,
                'file': obj.file
            }

        return self.get_objects(ids, EducationHistory, "EducationHistory", None, degree_name, degree_kwargs)

    def get_courses(self, ids):
        def courses_name(obj):
            return obj.course_name

        def courses_kwargs(obj):
            return {
                'fee': obj.fee,
            }

        return self.get_objects(ids, Courses, "Courses", None, courses_name, courses_kwargs)

    def get_student(self, ids):
        def student_name(obj):
            return obj.user.get_full_name()  

        def student_kwargs(obj):
            return {
                'student_id': obj.student_id,
                'date_of_admission': obj.date_of_admission,
                'shift': obj.shift,
            }

        return self.get_objects(ids, Students, "Students", None, student_name, student_kwargs)
    
    def get_enquiry(self, ids):
        def enquiry_subject(obj):
            return obj.subject

        def enquiry_kwargs(obj):
            return {
                'phone_number': obj.phone_number,
                'country': obj.get_country_display(),
                'message': obj.message
            }
        return self.get_objects(ids, Enquiry, "Enquiry", None, enquiry_subject, enquiry_kwargs)
    
    def get_events (self, ids):
        def events_title(obj):
            return obj.title

        def events_kwargs(obj):
            return {
                'event_type': obj.event_type,
                'title': obj.title,
            }
        return self.get_objects(ids, Event, "Event", None, events_title, events_kwargs)
    
    def get_blogs(self, ids):
        def blogs_title(obj):
            return obj.title

        def blogs_kwargs(obj):
            return {
                'date': obj.date,            
                'author': obj.author,        
                'content': obj.content     
            }
        return self.get_objects(ids, Blog, "Blog", None, blogs_title, blogs_kwargs)
    
    def get_titles(self, post_type: str, total):
        if post_type == "user":
            return "Users" if total > 1 else "User"
        elif post_type == "educational_history":
            return "EducationHistories" if total > 1 else "EducationHistory"
        elif post_type == "course":
            return "Courses" if total > 1 else "Course"
        elif post_type == "student":
            return "Students" if total > 1 else "Student"
        elif post_type == "enquiry":
            return "Enquiries" if total > 1 else "Enquiry"
        elif post_type == "event":
            return "Events" if total > 1 else "Event"
        elif post_type == "blog":
            return "Blogs" if total > 1 else "Blog"
        
        return "Objects"

    def get_delete_objects(self, delete_type, selected_ids=None):
        if selected_ids is None:
            selected_ids = []

        objects = []
        originals = []

        if selected_ids:
            if delete_type == "student":
                objects, originals = self.get_student(selected_ids)
            elif delete_type == "educational_history":
                objects, originals = self.get_educational_history(selected_ids)
            elif delete_type == "course":
                objects, originals = self.get_courses(selected_ids)
            elif delete_type == "user":
                objects, originals = self.get_user(selected_ids)
            elif delete_type == "enquiry":
                objects, originals = self.get_enquiry(selected_ids)
            elif delete_type == "event":
                objects, originals = self.get_events(selected_ids)
            elif delete_type == "blog":
                objects, originals = self.get_blogs(selected_ids)
        
        return objects, originals


class DeleteFinalView(View, DeleteHelper):
    def get(self, request, *args, **kwargs):
        return redirect("dashboard:index")

    def post(self, request, *args, **kwargs):
        delete_type = request.POST.get("_selected_type", None)
        selected_ids = request.POST.getlist("_selected_id", [])
        back = request.POST.get("_back_url", None)
        objects, originals = self.get_delete_objects(delete_type, selected_ids)

        for original in originals:
            try:
                object_title = original.id
                original.delete()
                messages.success(request, f"Successfully deleted #{object_title}")
            except Exception as e:
                messages.error(request, str(e))

        if back:
            return redirect(back)
        return redirect("dashboard:index")


@method_decorator(csrf_exempt, name='dispatch')
class DeleteView(View, DeleteHelper):
    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist("_selected_id", [])
        delete_type = request.POST.get("_selected_type", None)
        back = request.POST.get("_back_url", None)
        objects, originals = self.get_delete_objects(delete_type, selected_ids)

        # if not objects:
        #     raise Exception("No objects to delete")

        total_objects = len(objects)
        return render(request, 'dashboard/delete.html', context={
            "objects": objects,
            "type_title": self.get_titles(delete_type, total_objects),
            "back": back,
            "type": delete_type,
            "total": total_objects
        })
