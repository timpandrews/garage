from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.rides.views import (
    RideListView, RideDetailView, RideCreateView, RideUpdateView, RideDeleteView)

class TestRidesUrls(SimpleTestCase):
        def test_rides_list_url_is_resolved(self):
            url = reverse('rides:all')
            self.assertEquals(resolve(url).func.view_class, RideListView)

        def test_rides_list_url_login_required(self):
            response = self.client.get(reverse('rides:all'))
            self.assertTrue(response.url.startswith('/accounts/login/'))

        def test_rides_detail_url_is_resolved(self):
            url = reverse('rides:detail', args=[1])
            self.assertEquals(resolve(url).func.view_class, RideDetailView)

        def test_rides_create_url_is_resolved(self):
            url = reverse('rides:create')
            self.assertEquals(resolve(url).func.view_class, RideCreateView)

        def test_rides_update_url_is_resolved(self):
            url = reverse('rides:update', args=[1])
            self.assertEquals(resolve(url).func.view_class, RideUpdateView)

        def test_rides_delete_url_is_resolved(self):
            url = reverse('rides:delete', args=[1])
            self.assertEquals(resolve(url).func.view_class, RideDeleteView)