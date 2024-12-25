import unittest
from form_validator.validator import is_valid_email, is_strong_password, is_valid_mobile, is_18_or_older

class TestFormValidator(unittest.TestCase):

    def test_email(self):
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertFalse(is_valid_email("invalid-email"))

    def test_password(self):
        self.assertTrue(is_strong_password("Strong@123"))
        self.assertFalse(is_strong_password("weak"))

    def test_mobile(self):
        self.assertTrue(is_valid_mobile("9876543210"))
        self.assertFalse(is_valid_mobile("123456789"))

    def test_age(self):
        self.assertTrue(is_18_or_older("2000-01-01"))
        self.assertFalse(is_18_or_older("2010-01-01"))

if __name__ == "__main__":
    unittest.main()
