from unittest import TestCase, main
from SchoolSDK.client import Human, Teacher
from SchoolSDK.exceptions import *

class TestHuman(TestCase):
    def test_init(self):
        example_human = Human('Example', 43, 'male')
        self.assertTrue(example_human.name == 'Example' and example_human.age == 43 and example_human.gender == 'male')


    def test_setters_error_handling(self):
        example_human = Human('Example', 38, 'male')
        def set_human_age(new_age):
            example_human.age = new_age
        
        with self.assertRaises(NameAssignmentError):
            set_human_age(-1)


class TestTeacher(TestCase):
    def test_init(self):
        example_teacher = Teacher('Example', 43, 'male')
        self.assertTrue(example_teacher.name == 'Example' and example_teacher.age == 43 and example_teacher.gender == 'male')

    def test_setters(self):
        example_teacher = Teacher('Example', 43, 'male')
        example_teacher.name = 'Mosh'
        example_teacher.age = 20
        example_teacher.gender = 'female'
        self.assertTrue(example_teacher.name == 'Mosh' and example_teacher.age == 20 and example_teacher.gender == 'female')

    def test_getters(self):
        example_teacher = Teacher('Example', 38, 'male')
        self.assertTrue(example_teacher.name == 'Example' and example_teacher.age == 38 and example_teacher.gender == 'male')

    def test_setters_error_handling(self):
        example_teacher = Teacher('Example', 38, 'male')
        def set_teacher_name(new_name):
            example_teacher.name = new_name
        
        with self.assertRaises(NameAssignmentError):
            set_teacher_name(123)


if __name__ == '__main__':
    main()
