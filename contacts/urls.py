from django.conf.urls import patterns, include, url
from contacts.views import *

urlpatterns = patterns('',
    #url(r'^contacts/$', ContactsListView.as_view(), name='list'),
    url(r'^contacts/?$', TemplateView.as_view(template_name='contacts/base.html'), name='list'),
    url(r'^contacts/(?P<pk>\d+)/?$', ContactsDetailView.as_view(), name='detail'),
    url(r'^contacts/new/?$', ContactsCreateView.as_view(), name='new'),
    url(r'^contacts/upload/?$', 'contacts.views.contact_upload_form', name='upload'),

    url(r'^partials/(?P<template>[-\w]+)/?$', 'contacts.views.get_template'),

    url(r'^tags/?$', TagsListView.as_view(), name='tags-list'),


    url(r'^api/contacts/?$', ContactListCreateView.as_view()),
    url(r'^api/contacts/(?P<pk>\d+)/?$', ContactDetailAPIView.as_view()),
    url(r'^api/tags/?$', TagListCreateView.as_view()),
    url(r'^api/tags/(?P<pk>\d+)/?$', TagDetailAPIView.as_view()),
)
