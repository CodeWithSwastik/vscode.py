class Undefined:
    """
    An instance of this class is returned everytime javascript returns undefined.
    """

    def __str__(self):
        return "undefined"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__)


undefined = Undefined()
