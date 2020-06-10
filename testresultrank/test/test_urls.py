from django.test import SimpleTestCase
from django.urls import reverse, resolve
from testresultrank.views import resultanalyse

class testUrls(SimpleTestCase):
    def test_resultanalyse_url_is_resolved(self):
        url = reverse('resultanalyse')
        print(resolve(url))
        self.assertEquals(resolve(url).func, resultanalyse)