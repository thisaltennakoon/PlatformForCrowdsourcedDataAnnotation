from django.test import SimpleTestCase
from django.urls import reverse, resolve
from TextDataAnalyse.views import textanalyse

class testUrls(SimpleTestCase):
    def test_Textanalyse_url_is_resolved(self):
        url = reverse('textanalyse')
        print(resolve(url))
        self.assertEquals(resolve(url).func, textanalyse)