from django.test import TestCase, Client
from django.urls import reverse
from CreateTask.models import Task
import json

# class CreateTaskTest(TestCase):

#     def test_create_ImageAnnoTask(self):
#         client = Client()
#         #response = client.get(reverse('createtask:Anno_task_add'))

#         #self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(responsem, 'createtask/new.html')
