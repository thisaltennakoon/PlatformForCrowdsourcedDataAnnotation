from django.test import SimpleTestCase
from django.urls import reverse,resolve
from CreateTask.views import createTask,createTextTask,AddTextAnnoExamples,AddMediaAnnoExamples,DoTextAnnotationTest,DoMediaAnnotationTest
class TestUrls(SimpleTestCase):
    
    def test_cretetask_url_is_resolved(self):
        url = reverse('createtask:Anno_task_add')
        print(resolve(url))
        self.assertEquals(resolve(url).func, createTask)
    
    def test_createTextTask_url_is_resolved(self):
        url = reverse('createtask:TextAnno_task_add')
        print(resolve(url))
        self.assertEquals(resolve(url).func, createTextTask)

    def test_MediaAnno_example_add_url_is_resolved(self):
        url = reverse('createtask:MediaAnno_example_add', kwargs={'task_id': 1})
        print(resolve(url))
        self.assertEquals(resolve(url).func, AddMediaAnnoExamples)

    def test_TextAnno_example_add_url_is_resolved(self):
        url = reverse('createtask:TextAnno_example_add', kwargs={'task_id': 1})
        print(resolve(url))
        self.assertEquals(resolve(url).func, AddTextAnnoExamples)

    def test_TextAnno_Test_url_is_resolved(self):
        url = reverse('createtask:TextAnno_Test',kwargs={'task_id': 1})
        print(resolve(url))
        self.assertEquals(resolve(url).func, DoTextAnnotationTest)

    def test_ImageAnno_Test_url_is_resolved(self):
        url = reverse('createtask:ImageAnno_Test',kwargs={'task_id': 1})
        print(resolve(url))
        self.assertEquals(resolve(url).func, DoMediaAnnotationTest)
