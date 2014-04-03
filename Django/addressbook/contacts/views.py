# Create your views here.
from contacts.models import Contact, Bill
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
import datetime as dt

def HelloWorld(request):
    return HttpResponse("Hello world")

def CurDateTime(request):
    return HttpResponse(dt.datetime.now())

def FutureDateTime(request, offset):
    nt = dt.datetime.now() + dt.timedelta(hours=int(offset))
    return HttpResponse(nt)

class ReceiptView(DetailView):
    template_name = 'bill.html'
    model = Bill
    slug_field = 'person_name'

class ListContactView(ListView):
    model = Contact
    template_name = 'contact_list.html'

class CreateContactView(CreateView):
    model = Contact
    template_name = 'edit_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')
