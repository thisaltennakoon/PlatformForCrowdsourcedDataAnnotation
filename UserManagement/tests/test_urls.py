from django.test import SimpleTestCase
from django.urls import reverse, resolve
from UserManagement.views import sign_in

class TestUrls(SimpleTestCase):
    
    def test_list_url_is_resolved(self):
        user = 3
        url = reverse('sign_in', args=[user])
        print (resolve(url))
        #self.assertEquals(resolve(url).func, sign_in)