from .config import GRADES, GENDERS

# Helper functions

def age_is_valid(age):
    return age > 0

def gender_is_valid(gender):
    return gender in GENDERS

def grade_is_valid(grade):
    return grade in GRADES
