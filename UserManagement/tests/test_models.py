from django.test import TestCase
from UserManagement.models import *

class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(first_name="Bob",
                                last_name="Ben",
                                field = "Engineering",
                                country = "LK",
                                email = "bob@gmail.com",
                                bio = "I am an annotator"
                                )
    def test_first_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first_name')

    def test_first_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 255)