from django.test import TestCase,Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import *
from .models import *


class TestUrls(SimpleTestCase):

    def test_test_url_is_resolved(self):
        url = reverse('test')
        self.assertEquals(resolve(url).func, test)

    def test_task_url_is_resolved(self):
        url = reverse('task')
        self.assertEquals(resolve(url).func, task)

    def test_view_my_annotations_url_is_resolved(self):
        url = reverse('view_my_annotations')
        self.assertEquals(resolve(url).func, view_my_annotations)

    def test_view_my_annotations_change_url_is_resolved(self):
        url = reverse('view_my_annotations_change')
        self.assertEquals(resolve(url).func, view_my_annotations_change)

    def test_skip_data_instance_url_is_resolved(self):
        url = reverse('skip_data_instance')
        self.assertEquals(resolve(url).func, skip_data_instance)

    def test_stop_annotating_url_is_resolved(self):
        url = reverse('stop_annotating')
        self.assertEquals(resolve(url).func, stop_annotating)


class TestViews(TestCase):

    def test_testgtgt_GET(self):
        client = Client()
        #response = client.get(reverse('test'))

        #self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'DoDataAnnotationTask/test.html')
