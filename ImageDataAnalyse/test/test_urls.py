from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ImageDataAnalyse.views import Imageanalyse

class testUrls(SimpleTestCase):
    def test_Imageanalyse_url_is_resolved(self):
        url = reverse('Imageanalyse')
        print(resolve(url))
        self.assertEquals(resolve(url).func, Imageanalyse)