import unittest

# import data store
import es_store as ds

# import test data
from test_data import contacts

class TestAddressBook(unittest.TestCase):
    """Unit tests for address book CRUD operations."""

    def test_01_create(self):
        """Test create opertions."""

        self.assertEqual(ds.create_contact(contacts[0])['status'], 201)
        # out of bounds
        self.assertEqual(ds.create_contact(contacts[1])['status'], 400)
        self.assertEqual(ds.create_contact(contacts[2])['status'], 201)
        self.assertEqual(ds.create_contact(contacts[3])['status'], 201)
        self.assertEqual(ds.create_contact(contacts[4])['status'], 201)
        self.assertEqual(ds.create_contact(contacts[5])['status'], 201)
        self.assertEqual(ds.create_contact(contacts[6])['status'], 201)
        self.assertEqual(ds.create_contact(contacts[7])['status'], 201)
        # duplicate
        self.assertEqual(ds.create_contact(contacts[1])['status'], 400)


    def test_02_read(self):
        """Test read operations."""
        
        self.assertEqual(ds.read_contact(contacts[0]['name'])['name'], contacts[0]['name'])
        self.assertEqual(ds.read_contact(contacts[4]['name'])['phone'], contacts[4]['phone'])
        self.assertEqual(ds.read_contact(contacts[5]['name'])['email'], contacts[5]['email'])
        self.assertEqual(ds.read_contact(contacts[7]['name'])['address'], contacts[7]['address'])
    

    def test_03_update(self):
        """Test update operations."""

        self.assertEqual(ds.update_contact(contacts[0]['name'], contacts[2])['status'], 200)
        self.assertEqual(ds.read_contact(contacts[0]['name'])['phone'], contacts[2]['phone'])

        # out of bounds
        self.assertEqual(ds.update_contact(contacts[4]['name'], contacts[1])['status'], 400)

        self.assertEquals(ds.update_contact(contacts[1]['name'], contacts[5])['status'], 404)
    

    def test_04_delete(self):
        """Test delete operations."""

        self.assertEqual(ds.delete_contact(contacts[3]['name'])['status'], 200)
        self.assertEqual(ds.delete_contact(contacts[3]['name'])['status'], 404)
    

    def test_05_search(self):
        """Test search operations."""

        self.assertEqual(len(ds.search_contacts(10, 1, contacts[4]['name'] + ' OR ' + contacts[6]['name'])), 2)


if __name__ == '__main__':
    unittest.main()