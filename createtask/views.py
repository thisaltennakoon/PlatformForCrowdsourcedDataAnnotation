from django.shortcuts import render
from .models import AnnotationTask
from django.views.generic.edit import CreateView

class AnnotationTaskCreate(CreateView):
    model = AnnotationTask
    fields = ['title', 'decription', 'instructions']