from django.test import TestCase
from ..repository import Repository
from ..newegg_scrape import NewEggData
from ..memoryc_scrape import MemoryCData
from ..models import Part, Price, Catagory, Merchant
import mock
from django.test.client import RequestFactory

# Create your tests here.
class RepositoryTest(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self) -> None:
        self.repo = Repository()

        self.part_dict_valid = {
                "link" : "https://parts.com",
                "long_name": "Name of valid part",
                "brand" : "Valid industries",
                "image" : "https://picture.com/valid-part",
                "catagory" : self.repo.get_catagory_by_name('CPU'),
                "merchant" : self.repo.get_merchant_by_name('NewEgg'),
                "valid" : True,
                }
        self.part_dict_invalid = {
                "link" : "https://parts.com",
                "long_name": "Name of invalid part",
                "brand" : "Invalid industries",
                "image" : "https://picture.com/invalid-part",
                "catagory" : self.repo.get_catagory_by_name('CPU'),
                "merchant" : self.repo.get_merchant_by_name('NewEgg'),
                "valid" : False,
                }
        
        
    def test_get_catagories(self):
        # Arrange
        expected_length = 9
        expected_first = 'Operating System'
        expected_last = 'CPU'
        # Act
        catagories = self.repo.get_catagories()
        cat_length = len(catagories)
        first = catagories[0].name
        last = catagories[cat_length - 1].name
        # Assert
        self.assertEquals(cat_length, expected_length)
        self.assertEquals(first, expected_first)
        self.assertEquals(last, expected_last)
        
    def test_get_cata_byname(self):
        # Arrange
        expected = 'Case'
        # Act
        cata = self.repo.get_catagory_by_name('Case')
        actual = cata.name
        # Assert
        self.assertEquals(actual, expected)
    
    def test_get_cata_byid_1(self):
        # Arrange
        expected = 'CPU'
        # Act
        cat = self.repo.get_catagory_by_id(1)
        actual = cat.name
        # Assert
        self.assertEquals(actual, expected)
        
    def test_get_merchants(self):
        # Arrange
        expected_first = 'NewEgg'
        expected_second = 'MemoryC'
        expected_len = 2
        # Act
        merch = self.repo.get_merchants()
        merch_len = len(merch)
        first = merch[0].name
        second = merch[1].name
        # Assert
        self.assertEquals(merch_len, expected_len)
        self.assertEquals(first, expected_first)
        self.assertEquals(second, expected_second)
        
    def test_get_merchant_byname(self):
        # Arrange
        expected = 'NewEgg'
        name = 'NewEgg'
        # Act
        merch = self.repo.get_merchant_by_name(name)
        actual = merch.name
        # Assert
        self.assertEquals(actual, expected)
        
    def test_get_merchant_byid(self):
        # Arrange
        id = 2
        expected = 'MemoryC'
        # Act
        merch = self.repo.get_merchant_by_id(id)
        actual = merch.name
        # Assert
        self.assertEquals(actual, expected)

    def test_get_parts_first_and_last_ids(self):
        # Arrange
        first_expected_id = 1
        last_expected_id = 9
        # Act
        parts = self.repo.get_parts()
        first_actual_id = parts[0].id
        last_actual_id = parts[8].id
        # Assert
        self.assertEquals(first_expected_id, first_actual_id)
        self.assertEquals(last_expected_id, last_actual_id)

    def test_get_parts_by_catagory_name(self):
        # Arrange   
        expected = 2
        expected_len = 1
        # Act
        part = self.repo.get_parts_by_catagory_name('CPU Cooler')
        actual_len = len(part)
        actual = part[0].id
        # Assert
        self.assertEquals(actual, expected)
        self.assertEquals(actual_len, expected_len)

    def test_get_part_by_long_name(self):
        # Arrange
        expected = 3
        name = "GIGABYTE X570S AORUS ELITE AX AMD Ryzen 3000 PCIe 4.0 SATA 6Gb/s USB 3.2 AMD X570S ATX Motherboard"
        # Act
        part = self.repo.get_part_by_long_name(name)
        actual = part[0].id
        # Assert
        
        self.assertEquals(actual, expected)

    def test_get_part_by_id_4(self):
        # Arrange
        expected = 4
        id = 4
        # Act
        actual = self.repo.get_part_by_id(id).id
        # Assert
        self.assertEquals(actual, expected)

    # Cant figure out how to mock this. Moving on
    def test_create_part_from_scrape_valid(self):
        # Arrange
        expected = "https://picture.com/valid-part"
        # Act
        part = self.repo.create_part_from_scrape(self.part_dict_valid)
        actual = part.image
        # Assert
        self.assertEquals(actual, expected)

    def test_del_part_by_id(self):
        # Act
        self.repo.del_part_by_id(1)
        # # Assert
        with self.assertRaises(Part.DoesNotExist): 
            self.repo.get_part_by_id(1)

    def test_get_prices_both(self):
        # Arrange
        first_expected = 11998
        second_expected = 12098
        # Act
        prices = self.repo.get_prices()
        first_actual = prices[0].price
        second_actual = prices[1].price
        # Assert
        self.assertEquals(first_actual, first_expected)
        self.assertEquals(second_actual, second_expected)

    def test_get_prices_by_part_id_9(self):
        # Arrange
        part_id = 9
        expected = 12098
        # Act
        price = self.repo.get_prices_by_part_id(part_id)
        actual = price[1].price
        # Assert
        self.assertEquals(actual, expected)

    def test_get_price_by_id_1(self):
        # Arrange
        price_id = 1
        expected = 11998
        # Act
        actual = self.repo.get_price_by_id(price_id).price
        # Assert
        self.assertEquals(actual, expected)

    def test_del_price_by_id(self):
        # Act
        self.repo.del_price_by_id(1)
        # # Assert
        with self.assertRaises(Price.DoesNotExist): 
            self.repo.get_price_by_id(1)

    def test_create_newegg_screap(self):
        # Arrange
        rf = RequestFactory()
        post_request = rf.post('/', {'link' : 'https://fake.com',
                                     'catagory' : 'CPU'})
        expected = False
        # Act
        newegg_object = self.repo.create_newegg_scrape(post_request)
        actual = newegg_object.valid
        # Assert
        self.assertEquals(actual, expected)

    # def test_create_memoryC_scrape(self):
    #     # Arrange
    #     expected = ?
    #     # Act
    #     actual = ?
    #     # Assert
    #     self.assertEquals(actual, expected)
