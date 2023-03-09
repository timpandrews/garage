from django.test import SimpleTestCase # use simple test case when not using database
from django.urls import reverse, resolve

from apps.dashboard.views import dashboard, db_month, db_year

class TestUrls(SimpleTestCase):
        def test_dashboard_url_is_resolved(self):
            url = reverse('dashboard:dashboard')
            self.assertEquals(resolve(url).func, dashboard)

        def test_db_month_url_is_resolved(self):
            url = reverse('dashboard:db_month')
            self.assertEquals(resolve(url).func, db_month)

        def test_db_year_url_is_resolved(self):
            url = reverse('dashboard:db_year')
            self.assertEquals(resolve(url).func.view_class, db_year)