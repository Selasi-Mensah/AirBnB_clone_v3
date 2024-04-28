#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''this will test the FileStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in File Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_filestorage(self):
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except Exception:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except Exception:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    def test_z_all(self):
        """Tests expanded all functionality
        """
        storage = FileStorage()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        user_obj = storage.all(User)
        self.assertTrue(user_obj)
        state_obj = storage.all(State)
        self.assertFalse(state_obj)

    def test_z_delete(self):
        """Tests delete functionality
        """
        try:
            os.remove("file.json")
        except Exception:
            pass
        storage = FileStorage()
        state = State()
        state.name = "Maine"
        storage.new(state)
        self.assertTrue(storage.all(State))
        storage.delete(state)
        self.assertFalse(storage.all(State))

    def test_get(self):
        """Test that the get method properly retrievs objects"""
        storage = FileStorage()
        self.assertIs(storage.get("User", "blah"), None)
        self.assertIs(storage.get("blah", "blah"), None)
        new_user = User()
        new_user.save()
        self.assertIs(storage.get("User", new_user.id), new_user)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")

    def test_count(self):
        storage = FileStorage()
        initial_length = len(storage.all())
        self.assertEqual(storage.count(), initial_length)
        state_len = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), initial_length + 1)
        self.assertEqual(storage.count("State"), state_len + 1)


if __name__ == "__main__":
    unittest.main()
