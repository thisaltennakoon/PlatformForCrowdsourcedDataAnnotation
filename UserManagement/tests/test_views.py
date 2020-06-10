from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from UserManagement.views import *

class TestViews (TestCase):
    longMessage = True

    def test_search_is_resolved(self):
        factory = RequestFactory()
        RequestFactory = factory.get('UserManagement:search')
        response = search(request)
        self.assertEqual(200, response.status_code)