from django.http import HttpResponse
from django.shortcuts import get_object_or_404 
from django.views.generic import ListView, CreateView

from blog.models import Entry 
from blog.forms import CommentForm

class HomeView(ListView):
    template_name = "index.html"
    queryset = Entry.objects.order_by('-created_at')

home = HomeView.as_view()

class EntryDetail(CreateView):
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def get_entry(self):
        return get_object_or_404(Entry, pk=self.kwargs['pk'])

    def get_success_url(self):
        return self.get_entry().get_absolute_url()

    def dispatch(self, *args, **kwargs):
        self.entry = self.get_entry()
        return super(EntryDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['entry'] = self.entry
        return super(EntryDetail, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(EntryDetail, self).get_form_kwargs()
        kwargs['entry'] = self.entry
        return kwargs
        
entry_detail = EntryDetail.as_view()

