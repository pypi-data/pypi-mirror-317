from unittest import TestCase, main
from SchoolSDK.utils import *


class TestUtils(TestCase):
    def test_age_is_valid(self):
        self.assertEqual(age_is_valid(-1), False)
    
    def test_gender_is_valid(self):
        self.assertEqual(gender_is_valid('other gender'), False)
    
    def test_grade_is_valid(self):
        self.assertEqual(grade_is_valid('other gender'), False)


if __name__ == '__main__':
    main()
