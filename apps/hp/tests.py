from django.test import TestCase

# Test for the HPListView
class HPListViewTest(TestCase):
    def test_hp_list_view(self):
        response = self.client.get('/hp/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hp/hp_list.html')

