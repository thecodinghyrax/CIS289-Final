from django.test import TestCase
from ..repository import Repository
from ..newegg_scrape import NewEggData
from ..memoryc_scrape import MemoryCData
from ..models import Part, Price
import mock

# Create your tests here.
class RepositoryTest(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self) -> None:
        self.repo = Repository()


        
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
    # def test_createpart(self):
    #     # Arrange
    #     scraped_part_mock = mock.Mock(spec=NewEggData)
    #     scraped_part_mock.valid = True
    #     created_part_mock = mock.Mock()
    #     created_part_mock.long_name = "Second mocked Part"
    #     created_part_mock.save.return_value = True
    #     part_mock = mock.Mock(spec=Part)
    #     part_mock.long_name = "First mocked part"
    #     part_mock.objects = created_part_mock
    #     expected = True
    #     # Act
    #     actual = self.repo.create_part(scraped_part_mock)
    #     # Assert
    #     self.assertEquals(actual, expected)
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

    # def test_create_newegg_screap(self):
    #     # Arrange
    #     expected = ?
    #     # Act
    #     actual = ?
    #     # Assert
    #     self.assertEquals(actual, expected)

    # def test_create_memoryC_scrape(self):
    #     # Arrange
    #     expected = ?
    #     # Act
    #     actual = ?
    #     # Assert
    #     self.assertEquals(actual, expected)
