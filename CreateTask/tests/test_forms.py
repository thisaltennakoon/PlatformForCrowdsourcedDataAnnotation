from django.test import SimpleTestCase
from CreateTask.forms import CreateTaskForm,McqForm

class FormTest(SimpleTestCase):

    def test_CreateTaskForm_validData(self):
        taskform = CreateTaskForm(data={
            'title': 'task1', 
            'description': 'des1', 
            'instructions': 'ins1'
        })

        self.assertTrue(taskform.is_valid())

    def test_CreateTaskForm_NonvalidData(self):
        taskform = CreateTaskForm(data={
            'title': '', 
            'description': '', 
            'instructions': 'ins1'
        })

        self.assertFalse(taskform.is_valid())

    def test_McqForm_validData(self):
        mcqform = McqForm(data={
            'description ':'des1',
            'correctanswer' :'ans1',
            'option1':'o1',
            'option2':'o1',
            'option3':'o2',
            'option4' :'o3'
        })

        self.assertTrue(mcqform.is_valid())

    def test_McqForm_NonvalidData(self):
        mcqform = McqForm(data={
            'description ':'',
            'correctanswer' :'',
            'option1':'o1',
            'option2':'o1',
            'option3':'o2',
            'option4' :'o3'
        })

        self.assertFalse(mcqform.is_valid())