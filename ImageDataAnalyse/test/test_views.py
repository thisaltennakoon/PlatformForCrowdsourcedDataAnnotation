from django.test import TestCase,Client
from django.urls import reverse
from DoDataAnnotationTask.models import DataAnnotationResult as AnnotationDataSetresult
from CreateTask.models import Task, MediaDataInstance as AnnotationDataSet,Cateogary as DataClass
import json


