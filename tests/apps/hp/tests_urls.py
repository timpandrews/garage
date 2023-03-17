from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.hp.views import HPListView, HPDetailView, HPCreateView, HPUpdateView, HPDeleteView

class TestUrls(SimpleTestCase):
        def test_hp_list_url_is_resolved(self):
            url = reverse('hp:list')
            self.assertEquals(resolve(url).func.view_class, HPListView)

        def test_hp_detail_url_is_resolved(self):
            url = reverse('hp:detail', args=[1])
            self.assertEquals(resolve(url).func.view_class, HPDetailView)

        def test_hp_create_url_is_resolved(self):
            url = reverse('hp:create')
            self.assertEquals(resolve(url).func.view_class, HPCreateView)

        def test_hp_update_url_is_resolved(self):
            url = reverse('hp:update', args=[1])
            self.assertEquals(resolve(url).func.view_class, HPUpdateView)

        def test_hp_delete_url_is_resolved(self):
            url = reverse('hp:delete', args=[1])
            self.assertEquals(resolve(url).func.view_class, HPDeleteView)