from django.test import TestCase
from .repository import Repository

# Create your tests here.
class RepositoryTest(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self) -> None:
        self.repo = Repository()
    
    def test_repo_get_cata_byid_1(self):
        cat = self.repo.get_catagory_by_id(1)
        actual = cat.name
        expected = 'CPU'
        self.assertEquals(actual, expected)