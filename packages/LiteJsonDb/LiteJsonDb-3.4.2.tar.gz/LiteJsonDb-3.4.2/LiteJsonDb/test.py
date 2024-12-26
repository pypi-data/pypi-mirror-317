import unittest
from time import sleep
from LiteJsonDb import JsonDB

class TestJsonDB(unittest.TestCase):

    def setUp(self):
        self.db = JsonDB()
        print("🔧 Setup database")

    def test_set_data(self):
        self.db.set_data("posts")
        self.db.set_data("users/1", {"name": "Aliou", "age": 20})
        self.db.set_data("users/2", {"name": "Coder", "age": 25})
        print("✅ Data set")

    def test_edit_data(self):
        self.db.set_data("users/1", {"name": "Aliou", "age": 20})
        self.db.edit_data("users/1", {"name": "Alex"})
        user1 = self.db.get_data("users/1")
        self.assertEqual(user1["name"], "Alex")
        print("🔄 Data modified")

    def test_get_data(self):
        self.db.set_data("users/1", {"name": "Aliou", "age": 20})
        user1 = self.db.get_data("users/1")
        self.assertEqual(user1["name"], "Aliou")
        print("📋 Data retrieved")

    def test_remove_data(self):
        self.db.set_data("users/2", {"name": "Coder", "age": 25})
        self.db.remove_data("users/2")
        user2 = self.db.get_data("users/2")
        self.assertIsNone(user2)
        print("❌ Data removed")

    def test_search_data(self):
        self.db.set_data("users/1", {"name": "Aliou", "age": 20})
        results = self.db.search_data("Aliou")
        self.assertTrue(any("Aliou" in user.values() for user in results))
        print("🔍 Search results")

    def test_full_db(self):
        self.db.set_data("users/1", {"name": "Aliou", "age": 20})
        full_db = self.db.get_db(raw=True)
        self.assertIn("users", full_db)
        print("📚 Full database retrieved")

    def test_subcollection(self):
        self.db.set_subcollection("groups", "1", {"name": "Admins"})
        self.db.edit_subcollection("groups", "1", {"description": "Admin group"})
        groups = self.db.get_subcollection("groups")
        self.assertIn("1", groups)
        self.db.remove_subcollection("groups", "1")
        groups = self.db.get_subcollection("groups")
        self.assertNotIn("1", groups)
        print("🗂️ Subcollection operations")

    def tearDown(self):
        self.db = None
        print("🧹 Tear down database")

if __name__ == '__main__':
    unittest.main()
