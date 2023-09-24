class RequiresExtraError(ImportError):
    """
    Raise when a required extra is not installed
    """


class EmptyIteratorError(IndexError):
    """
    Raised if trying to perform an action an empty iterator
    which can not be done.
    """


class NotFoundError(IndexError):
    """
    Raised if no element matches the given predicate
    """


class StopScan(Exception):
    """
    Exception used to indicate that a `.scan()` should be stopped.
    Similar to StopIteration, but can be raised explicitely
    """
