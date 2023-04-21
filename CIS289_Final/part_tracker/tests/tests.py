from django.test import TestCase
from ..repository import Repository

# Create your tests here.
class RepositoryTest(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self) -> None:
        self.repo = Repository()
        
    def test_get_catagories(self):
        catagories = self.repo.get_catagories()
        cat_length = len(catagories)
        expected_length = 9
        first = catagories[0].name
        expected_first = 'Operating System'
        last = catagories[cat_length - 1].name
        expected_last = 'CPU'
        self.assertEquals(cat_length, expected_length)
        self.assertEquals(first, expected_first)
        self.assertEquals(last, expected_last)
        
    def test_get_cata_byname(self):
        cata = self.repo.get_catagory_by_name('Case')
        actual = cata.name
        expected = 'Case'
        self.assertEquals(actual, expected)
    
    def test_get_cata_byid_1(self):
        cat = self.repo.get_catagory_by_id(1)
        actual = cat.name
        expected = 'CPU'
        self.assertEquals(actual, expected)
        
    def test_get_merchants(self):
        merch = self.repo.get_merchants()
        merch_len = len(merch)
        expected_len = 2
        first = merch[0].name
        expected_first = 'NewEgg'
        second = merch[1].name
        expected_second = 'MemoryC'
        self.assertEquals(merch_len, expected_len)
        self.assertEquals(first, expected_first)
        self.assertEquals(second, expected_second)