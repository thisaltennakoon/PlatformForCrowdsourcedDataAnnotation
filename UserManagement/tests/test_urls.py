from django.test import SimpleTestCase
from django.urls import reverse, resolve
from UserManagement.views import *

class TestUrls(SimpleTestCase):


    def test_sign_up_is_resolved(self):
        url = reverse('UserManagement:sign_up')
        print (resolve(url))
        self.assertEquals(resolve(url).func, sign_up)

    def test_sign_in_is_resolved(self):
        url = reverse('UserManagement:sign_in')
        print (resolve(url))
        self.assertEquals(resolve(url).func, sign_in)

    def test_sign_out_is_resolved(self):
        url = reverse('UserManagement:sign_out')
        print (resolve(url))
        self.assertEquals(resolve(url).func, sign_out)

    def test_profile_is_resolved(self):
        url = reverse('UserManagement:profile')
        print (resolve(url))
        self.assertEquals(resolve(url).func, profile)
    
    def test_edit_profile_is_resolved(self):
        url = reverse('UserManagement:edit_profile')
        print (resolve(url))
        self.assertEquals(resolve(url).func, edit_profile)
   
    def test_change_password_is_resolved(self):
        url = reverse('UserManagement:change_password')
        print (resolve(url))
        self.assertEquals(resolve(url).func, change_password)

    def test_search_is_resolved(self):
        url = reverse('UserManagement:search')
        print (resolve(url))
        self.assertEquals(resolve(url).func, search)
