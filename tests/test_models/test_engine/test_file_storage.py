#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py."""
import os
import json
import pep8
import unittest
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Defines unittests for the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment before running the test cases."""
        try:
            os.rename("file.json", "test_file")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()
        key = "{}.{}".format(type(cls.base).__name__, cls.base.id)
        FileStorage._FileStorage__objects[key] = cls.base
        cls.user = User()
        key = "{}.{}".format(type(cls.user).__name__, cls.user.id)
        FileStorage._FileStorage__objects[key] = cls.user
        cls.state = State()
        key = "{}.{}".format(type(cls.state).__name__, cls.state.id)
        FileStorage._FileStorage__objects[key] = cls.state
        cls.place = Place()
        key = "{}.{}".format(type(cls.place).__name__, cls.place.id)
        FileStorage._FileStorage__objects[key] = cls.place
        cls.city = City()
        key = "{}.{}".format(type(cls.city).__name__, cls.city.id)
        FileStorage._FileStorage__objects[key] = cls.city
        cls.amenity = Amenity()
        key = "{}.{}".format(type(cls.amenity).__name__, cls.amenity.id)
        FileStorage._FileStorage__objects[key] = cls.amenity
        cls.review = Review()
        key = "{}.{}".format(type(cls.review).__name__, cls.review.id)
        FileStorage._FileStorage__objects[key] = cls.review

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment after running the test cases."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("test_file", "file.json")
        except IOError:
            pass
        del cls.storage
        del cls.base
        del cls.user
        del cls.state
        del cls.place
        del cls.city
        del cls.amenity
        del cls.review

    def test_docstrings_for_all_methods(self):
        """Check if all methods have docstrings."""
        self.assertIsNotNone(FileStorage.__doc__)
        self.assertIsNotNone(FileStorage.all.__doc__)
        self.assertIsNotNone(FileStorage.new.__doc__)
        self.assertIsNotNone(FileStorage.reload.__doc__)
        self.assertIsNotNone(FileStorage.delete.__doc__)

    def test_pep8_FileStorage(self):
        """Check if the FileStorage class follows PEP8 styling."""
        value = pep8.StyleGuide(quiet=True)
        printed = value.check_files(['models/engine/file_storage.py'])
        self.assertEqual(printed.total_errors, 0, "fix pep8")

    def test_methods(self):
        """Check if the FileStorage class has all the required methods."""
        self.assertTrue(hasattr(FileStorage, "all"))
        self.assertTrue(hasattr(FileStorage, "new"))
        self.assertTrue(hasattr(FileStorage, "reload"))
        self.assertTrue(hasattr(FileStorage, "delete"))

    def test_attributes(self):
        """Check if the FileStorage class has the required attributes."""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_init(self):
        """Test the initialization of the FileStorage class."""
        self.assertTrue(isinstance(self.storage, FileStorage))

    def test_all(self):
        """Test the default all() method of the FileStorage class."""
        new = self.storage.all()
        self.assertEqual(type(new), dict)
        self.assertIs(new, FileStorage._FileStorage__objects)
        self.assertEqual(len(new), 7)

    def test_all_cls(self):
        """Test the all() method of the FileStorage class with specified cls."""
        new = self.storage.all(BaseModel)
        self.assertEqual(type(new), dict)
        self.assertEqual(len(new), 1)
        self.assertEqual(self.base, list(new.values())[0])

    def test_new(self):
        """Test the new() method of the FileStorage class."""
        bm = BaseModel()
        self.storage.new(bm)
        store = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, store.keys())
        self.assertIn(self.base, store.values())

    def test_save(self):
        """Test the save() method of the FileStorage class."""
        self.storage.save()
        with open("file.json", "r", encoding="utf-8") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + self.base.id, save_text)
            self.assertIn("User." + self.user.id, save_text)
            self.assertIn("State." + self.state.id, save_text)
            self.assertIn("Place." + self.place.id, save_text)
            self.assertIn("City." + self.city.id, save_text)
            self.assertIn("Amenity." + self.amenity.id, save_text)
            self.assertIn("Review." + self.review.id, save_text)

    def test_reload(self):
        """Test the reload() method of the FileStorage class."""
        bm = BaseModel()
        with open("file.json", "w", encoding="utf-8") as f:
            key = "{}.{}".format(type(bm).__name__, bm.id)
            json.dump({key: bm.to_dict()}, f)
        self.storage.reload()
        store = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, store)

    def test_reload_no_file(self):
        """Test the reload() method of the FileStorage class with no existing file.json."""
        try:
            self.storage.reload()
        except Exception:
            self.fail

    def test_delete(self):
        """Test the delete() method of the FileStorage class."""
        bm = BaseModel()
        key = "{}.{}".format(type(bm).__name__, bm.id)
        FileStorage._FileStorage__objects[key] = bm
        self.storage.delete(bm)
        self.assertNotIn(bm, FileStorage._FileStorage__objects)

    def test_delete_nonexistent(self):
        """Test the delete() method of the FileStorage class with a nonexistent object."""
        try:
            self.storage.delete(BaseModel())
        except Exception:
            self.fail

if __name__ == "__main__":
    unittest.main()