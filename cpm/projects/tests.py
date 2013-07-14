from django.core.urlresolvers import reverse

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Project

TEXT_BLOCK = open('tests/lipsum.txt', 'r').read()


def create_project():
    user = User.objects.create(username='testuser', password='default')
    return Project.objects.create(title="Test Project", user=user, description=TEXT_BLOCK)


class ProjectCreateTest(TestCase):
    def test_get_absolute_url(self):
        new_project = create_project()
        self.assertEqual(new_project.get_absolute_url(), '/cpm/projects/1/')


class ProjectIndexDetailTests(TestCase):
    def test_detail_view_with_a_project(self):
        """
        The detail view of a project
        """
        new_project = create_project()
        response = self.client.get(reverse('projects:project-detail', args=(new_project.id,)))
        self.assertEqual(response.status_code, 404)
