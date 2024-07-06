from django.views.generic import ListView

from calendarapp.models.event import Event 


class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendar/calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user) # type: ignore


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendar/calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user) # type: ignore
