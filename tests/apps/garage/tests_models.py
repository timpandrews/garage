from django.contrib.auth.models import User
from django.test import TestCase

from apps.garage.models import Doc, Kudos, Profile, ZwiftRouteList


class TestUserAndProfileModel(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            username = 'testuser',
            email = 'testemail@test.com'
        )
        user.set_password('test123password')
        user.save()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)

    def test_profile_created_automatically(self):
        user = User.objects.create(
            username = 'testuser2',
            email = 'testemail2@test.com'
        )
        user.set_password('test123password')
        user.save()

        self.assertEqual(user.profile, Profile.objects.get(user=user))


class DocModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username = 'testuser',
            email = 'testemail@test.com'
        )
        user.set_password('test123password')
        user.save()

    def test_doc_creation(self):
        user = User.objects.get(username='testuser')
        doc = Doc.objects.create(
            doc_type = 'hp',
            doc_date = '2019-11-11',
            user = user,
            data = "{'test':'data'}"
        )
        self.assertTrue(isinstance(doc, Doc))
        self.assertEqual(doc.__str__(), doc.doc_type)


class KudosModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username = 'testuser',
            email = 'testemail@test.com'
        )
        user.set_password('test123password')
        user.save()

    def test_kudos_creation(self):
        user = User.objects.get(username='testuser')
        kudos = Kudos.objects.create(
            hex = '00007d',
            key = '001_00007d',
            user = user,
            type = 'test',
            data = "{'test':'data'}"
        )
        self.assertTrue(isinstance(kudos, Kudos))
        self.assertEqual(kudos.__str__(), kudos.key)


class ZwiftRouteListModelTest(TestCase):
    def setUp(self):
        ZwiftRouteList.objects.create(
            route_name = 'Ven-Top',
            world_name = 'France'
        )

    def test_get_world_name_by_route_name(self):
        obj = ZwiftRouteList.objects.get(route_name='Ven-Top')
        self.assertEqual(obj.world_name, 'France')
        self.assertTrue(isinstance(obj, ZwiftRouteList))






