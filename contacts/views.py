from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, TemplateView, FormView, DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseServerError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from contacts.helpers import handle_uploaded_file
import csv
import cStringIO

from contacts.models import Tag, Contact, Document
from contacts.forms import *
from contacts.serializers import ContactSerializer, TagSerializer


class TagListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    model = Tag

class TagDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    model = Tag

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ContactListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer
    model = Contact


class ContactDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer
    model = Contact

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
class ContactsListView(ListView):
    template_name = 'contacts/list.html'
    model = Contact
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        # Call the super
        context = super(ContactsListView, self).get_context_data(**kwargs)

        # Add in a queryset for Documents
        context['documents'] = Document.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class ContactsDetailView(DetailView):
    template_name = 'contacts/detail.html'
    model = Contact

class ContactsCreateView(CreateView):
    template_name = 'contacts/new.html'
    form_class = ContactsForm
    success_url = '/contacts/'

    def form_valid(self, form):
        a = Account.objects.get(admin=self.request.user.pk)
        form.set_account(a)
        return super(ContactsCreateView, self).form_valid(form)

def contact_upload_form(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            
            flashes = handle_uploaded_file(request.FILES['docfile'])
            
            return render(request, 'contacts/base.html', { 'flash': flashes })
#            return HttpResponseRedirect(reverse('list'))
    else:
        form = UploadFileForm()
        
        documents = Document.objects.all()
            
    return render(request, 'contacts/upload.html', {
            'documents': documents,
            'form': form,
            })

@login_required
def get_template(request, template):
    print template
    app, template = template.split('-')
    template_path = "%s/%s.html" % (app, template)
    return render(request, template_path)

class TagsListView(TemplateView):
    template_name = 'tags/list.html'

class TagsCreateView(CreateView):
    template_name = 'tags/new.html'
    success_url = '/tags/'
