#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
	TestReview_instantiation
	TestReview_save
	TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
	"""Unittests for testing instantiation of the Review class."""

	def test_no_args_instantiates(self):
    	self.assertEqual(Review, type(Review()))

	def test_new_instance_stored_in_objects(self):
    	self.assertIn(Review(), models.storage.all().values())

	def test_id_is_public_str(self):
    	self.assertEqual(str, type(Review().id))

	def test_created_at_is_public_datetime(self):
    	self.assertEqual(datetime, type(Review().created_at))

	def test_updated_at_is_public_datetime(self):
    	self.assertEqual(datetime, type(Review().updated_at))

	def test_place_id_is_public_class_attribute(self):
    	rw = Review()
    	self.assertEqual(str, type(Review.place_id))
    	self.assertIn("place_id", dir(rw))
    	self.assertNotIn("place_id", rw.__dict__)

	def test_user_id_is_public_class_attribute(self):
    	rw = Review()
    	self.assertEqual(str, type(Review.user_id))
    	self.assertIn("user_id", dir(rw))
    	self.assertNotIn("user_id", rw.__dict__)

	def test_text_is_public_class_attribute(self):
    	rw = Review()
    	self.assertEqual(str, type(Review.text))
    	self.assertIn("text", dir(rw))
    	self.assertNotIn("text", rw.__dict__)

	def test_two_reviews_unique_ids(self):
    	rw1 = Review()
    	rw2 = Review()
    	self.assertNotEqual(rw1.id, rw2.id)

	def test_two_reviews_different_created_at(self):
    	rw1 = Review()
    	sleep(0.05)
    	rw2 = Review()
    	self.assertLess(rw1.created_at, rw2.created_at)

	def test_two_reviews_different_updated_at(self):
    	rw1 = Review()
    	sleep(0.05)
    	rw2 = Review()
    	self.assertLess(rw1.updated_at, rw2.updated_at)

	def test_str_representation(self):
    	dt = datetime.today()
    	dt_repr = repr(dt)
    	rw = Review()
    	rw.id = "123456"
    	rw.created_at = rw.updated_at = dt
    	rwstr = rw.__str__()
    	self.assertIn("[Review] (123456)", rwstr)
    	self.assertIn("'id': '123456'", rwstr)
    	self.assertIn("'created_at': " + dt_repr, rwstr)
    	self.assertIn("'updated_at': " + dt_repr, rwstr)

	def test_args_unused(self):
    	rw = Review(None)
    	self.assertNotIn(None, rw.__dict__.values())

	def test_instantiation_with_kwargs(self):
    	dt = datetime.today()
    	dt_iso = dt.isoformat()
    	rw = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
    	self.assertEqual(rw.id, "345")
    	self.assertEqual(rw.created_at, dt)
    	self.assertEqual(rw.updated_at, dt)

	def test_instantiation_with_None_kwargs(self):
    	with self.assertRaises(TypeError):
        	Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
	"""Unittests for testing save method of the Review class."""

	@classmethod
	def setUp(self):
    	try:
        	os.rename("file.json", "tmp")
    	except IOError:
        	pass

	def tearDown(self):
    	try:
        	os.remove("file.json")
    	except IOError:
        	pass
    	try:
        	os.rename("tmp", "file.json")
    	except IOError:
        	pass

	def test_one_save(self):
    	rw = Review()
    	sleep(0.05)
    	first_updated_at = rw.updated_at
    	rw.save()
    	self.assertLess(first_updated_at, rw.updated_at)

	def test_two_saves(self):
    	rw = Review()
    	sleep(0.05)
    	first_updated_at = rw.updated_at
    	rw.save()
    	second_updated_at = rw.updated_at
    	self.assertLess(first_updated_at, second_updated_at)
    	sleep(0.05)
    	rw.save()
    	self.assertLess(second_updated_at, rw.updated_at)

	def test_save_with_arg(self):
    	rw = Review()
    	with self.assertRaises(TypeError):
        	rw.save(None)

	def test_save_updates_file(self):
    	rw = Review()
    	rw.save()
    	rwid = "Review." + rw.id
    	with open("file.json", "r") as f:
        	self.assertIn(rwid, f.read())


class TestReview_to_dict(unittest.TestCase):
	"""Unittests for testing to_dict method of the Review class."""

	def test_to_dict_type(self):
    	self.assertTrue(dict, type(Review().to_dict()))

	def test_to_dict_contains_correct_keys(self):
    	rw = Review()
    	self.assertIn("id", rw.to_dict())
    	self.assertIn("created_at", rw.to_dict())
    	self.assertIn("updated_at", rw.to_dict())
    	self.assertIn("__class__", rw.to_dict())

	def test_to_dict_contains_added_attributes(self):
    	rw = Review()
    	rw.middle_name = "Holberton"
    	rw.my_number = 98
    	self.assertEqual("Holberton", rw.middle_name)
    	self.assertIn("my_number", rw.to_dict())

	def test_to_dict_datetime_attributes_are_strs(self):
    	rw = Review()
    	rw_dict = rw.to_dict()
    	self.assertEqual(str, type(rw_dict["id"]))
    	self.assertEqual(str, type(rw_dict["created_at"]))
    	self.assertEqual(str, type(rw_dict["updated_at"]))

	def test_to_dict_output(self):
    	dt = datetime.today()
    	rw = Review()
    	rw.id = "123456"
    	rw.created_at = rw.updated_at = dt
    	tdict = {
        	'id': '123456',
        	'__class__': 'Review',
        	'created_at': dt.isoformat(),
        	'updated_at': dt.isoformat(),
    	}
    	self.assertDictEqual(rw.to_dict(), tdict)

	def test_contrast_to_dict_dunder_dict(self):
    	rw = Review()
    	self.assertNotEqual(rw.to_dict(), rw.__dict__)

	def test_to_dict_with_arg(self):
    	rw = Review()
    	with self.assertRaises(TypeError):
        	rw.to_dict(None)


if __name__ == "__main__":
	unittest.main()
