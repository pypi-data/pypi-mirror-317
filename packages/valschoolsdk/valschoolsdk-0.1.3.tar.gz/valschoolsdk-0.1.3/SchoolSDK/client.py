# School Classes
from .exceptions import NameAssignmentError, AgeAssignmentError, GradeAssignmentError, GenderAssignmentError
from .config import GENDERS, GRADES

class Human:
    """Base class for the `Teacher` and `Student` class. These classes both inherit common functionalities from this class."""
    def __init__(self, name, age, gender):
        self._name = name
        self._age = age
        self._gender = gender
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise NameAssignmentError('Name must be of type str!')
        self._name = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if value < 1:
            raise AgeAssignmentError('Age must be greater than 0')
        self._age = value

    @property
    def gender(self):
        return self._gender
    
    @gender.setter
    def gender(self, value):
        if value not in GENDERS:
            raise GenderAssignmentError('Gender must be male or female')
        self._gender = value

    

class Teacher(Human):
    """Instantiate this class to create a `Teacher` object"""
    def __str__(self):
        return "Teacher {}".format(self.name)

    def teach(self):
        print('I am teaching')


class Student(Human):
    """Instantiate this class to create a `Student` object"""
    def __init__(self, name, age, gender, grade):
        super().__init__(name, age, gender)
        self._grade = grade
    
    def __str__(self):
        return "Teacher {}".format(self.name)
    
    @property
    def grade(self):
        return self._grade
    
    @grade.setter
    def grade(self, value):
        if value not in GRADES:
            raise GradeAssignmentError(f'Grade must be in {GRADES}')
        self._grade = value

    def learn(self):
        print('I am learning')
        
