# Custom Exceptions

class SDKException(Exception):
    pass


class NameAssignmentError(SDKException):
    pass


class AgeAssignmentError(SDKException):
    pass


class GradeAssignmentError(SDKException):
    pass


class GenderAssignmentError(SDKException):
    pass