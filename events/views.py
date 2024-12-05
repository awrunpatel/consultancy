from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import get_token
from .models import Event
from .forms import EventForm


class EventsListView(View):
    template_name = 'dashboard/events/list.html'

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        return render(request, self.template_name, {
            'events': events
        })


class EventsView(View):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        if event_id:
            event = get_object_or_404(Event, id=event_id)
            form = EventForm(instance=event)
            title = "Update Event"
        else:
            form = EventForm()
            title = "Create Event"

        return render(request, 'dashboard/events/events.html', context={
            'form': form,
            'title': title,
            'pk': event_id
        })

    def post(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        if event_id:
            event = get_object_or_404(Event, id=event_id)
            form = EventForm(request.POST, instance=event)
        else:
            form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            if event_id:
                messages.success(request, "Event updated successfully.")
            else:
                messages.success(request, "Event created successfully.")
            return redirect('events:events')

        title = "Update Event" if event_id else "Create Event"
        return render(request, 'dashboard/events/events.html', context={
            'form': form,
            'title': title,
            'pk': event_id
        })


class EventsAjaxView(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        events = Event.objects.all().order_by("start_date")

        if search_value:
            events = events.filter(title__icontains=search_value)

        paginator = Paginator(events, length)

        try:
            page_events = paginator.page(page_number)
        except EmptyPage:
            page_events = []

        data = []
        for event in page_events:
            data.append(
                [
                    event.title,
                    event.event_type,
                    event.start_date.strftime('%Y-%m-%d') if event.start_date else "N/A",
                    event.end_date.strftime('%Y-%m-%d') if event.end_date else "N/A",
                    "Online" if event.is_online else "Offline",
                    "Active" if event.is_active else "Inactive",
                    self.get_action(event.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": Event.objects.count(),
                "recordsFiltered": events.count(),
                "data": data,
            },
            status=200,
        )

    def get_action(self, event_id):
        request = self.request
        csrf_token = get_token(request)

        edit_url = reverse('events:events_update', kwargs={'pk': event_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('events:events')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{event_id}" />
                <input type="hidden" name="_selected_type" value="event" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
