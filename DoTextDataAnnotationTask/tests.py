from django.test import TestCase,Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import *
from .models import *
from CreateTask.models import Task,TextDataInstance
from django.contrib.auth.models import User,Group
import datetime


class TestUrls(SimpleTestCase):

    def test_task_url_is_resolved(self):
        url = reverse('do_text_data_annotation_task')
        self.assertEquals(resolve(url).func, task)

    def test_view_my_annotations_url_is_resolved(self):
        url = reverse('do_text_data_annotation_view_my_annotations')
        self.assertEquals(resolve(url).func, view_my_annotations)

    def test_view_my_annotations_change_url_is_resolved(self):
        url = reverse('do_text_data_annotation_view_my_annotations_change')
        self.assertEquals(resolve(url).func, view_my_annotations_change)

    def test_skip_data_instance_url_is_resolved(self):
        url = reverse('do_text_data_annotation_skip_data_instance')
        self.assertEquals(resolve(url).func, skip_data_instance)

    def test_stop_annotating_url_is_resolved(self):
        url = reverse('do_text_data_annotation_stop_annotating')
        self.assertEquals(resolve(url).func, stop_annotating)



class TestModels(TestCase):

    def setUp(self):
        self.my_user = User.objects.create(username='Author')
        self.task=Task.objects.create(creatorID=self.my_user,
                            title="test title",
                            description="test description",
                            status="test status",
                            instructions="test instructions",
                            field="test field",
                            taskType="test taskType",
                            requiredNumofAnnotations=3)
        self.data_instance1 = TextDataInstance.objects.create(taskID=self.task,
                                                              LastUpdate=datetime.datetime.now())
        self.data_instance2 = TextDataInstance.objects.create(taskID=self.task,
                                                              LastUpdate=datetime.datetime.now())

    def test_DataAnnotationResult(self):
        contributor_user = User.objects.create(username='Contributor')
        data_instances = TextDataInstance.objects.filter(taskID=self.task)
        for data_instance in data_instances:
            data_instance.IsViewing = True
            data_instance.WhoIsViewing = contributor_user.id
            data_instance_reserved_time = datetime.datetime.now()
            data_instance.LastUpdate = data_instance_reserved_time
            data_instance.save()
            self.assertEqual(data_instance.IsViewing, True)
            self.assertEqual(data_instance.WhoIsViewing, contributor_user.id)
            self.assertEqual(data_instance.LastUpdate, data_instance_reserved_time)
            DataAnnotationResult.objects.create(TaskID=self.task,
                                                                         DataInstance=data_instance,
                                                                         ClassID=0,
                                                                         UserID=contributor_user.id,
                                                                         LastUpdate=datetime.datetime.now())
            data_instance.IsViewing = False
            data_instance.WhoIsViewing = 0
            data_instance_released_time = datetime.datetime.now()
            data_instance.LastUpdate = data_instance_released_time
            data_instance.save()
            self.assertEqual(data_instance.IsViewing, False)
            self.assertEqual(data_instance.WhoIsViewing, 0)
            self.assertEqual(data_instance.LastUpdate, data_instance_released_time)


#class TestViews(TestCase):

    #def setUp(self):
        #group_name = "My Test Group"
        #self.group = Group(name=group_name)
        #self.group.save()
        #self.c = Client()
        #self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        #print(self.group)

    #def test_testgtgt_GET(self):
        #client = Client()
        #response = client.get('test')

        #self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'DoDataAnnotationTask/test.html')


    #def test_user_can_access(self):
        #self.user.groups.add(self.group)
        #self.user.save()
        #self.c.login(username='test', password='test')
        #response = self.c.get("/DoDataAnnotationTask/task")
        #self.assertEqual(response.status_code, 200)