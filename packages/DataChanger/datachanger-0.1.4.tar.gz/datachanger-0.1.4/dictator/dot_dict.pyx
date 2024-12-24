from cpython.dict cimport PyDict_New, PyDict_SetItem
from json import loads  # For handling JSON data

cdef class DotDict:
    cdef dict __dict__  # Dictionary to store attributes
    cdef bint raise_error  # Flag to control error raising
    cdef bint convert_iterables  # Flag to control iterable conversion

    def __cinit__(self, input_data=None, bint raise_error=True, bint convert_iterables=False):
        """Initialize the DotDict with a dictionary or JSON string."""
        self.__dict__ = PyDict_New()
        self.raise_error = raise_error
        self.convert_iterables = convert_iterables
        if input_data:
            self._load_data(input_data)

    cdef void _load_data(self, input_data):
        """Load data from a dictionary or JSON string."""
        if isinstance(input_data, str):
            input_data = loads(input_data)  # Convert JSON string to dict

        if isinstance(input_data, dict):
            self._load_dict(input_data)
        else:
            raise ValueError("Input data must be a dictionary or a valid JSON string.")

    cdef void _load_dict(self, dict input_dict):
        """Load data into the dictionary."""
        cdef object key, value
        for key, value in input_dict.items():
            PyDict_SetItem(self.__dict__, key, self._wrap_value(value))

    cdef object _wrap_value(self, value):
        """Wrap the value into an appropriate type."""
        if isinstance(value, dict):
            return DotDict(value, self.raise_error, self.convert_iterables)  # Pass convert_iterables flag
        elif isinstance(value, list):
            return self._wrap_iterable(value)  # Handle lists
        elif isinstance(value, tuple):
            return self._wrap_iterable(value)  # Handle tuples
        elif isinstance(value, set):
            return self._wrap_iterable(value)  # Handle sets
        else:
            return value  # Leave primitive values as-is

    cdef object _wrap_iterable(self, iterable):
        """Wrap nested dictionaries inside iterables (list, tuple, set) as DotDict objects."""
        cdef list result = []
        for item in iterable:
            if isinstance(item, dict):
                result.append(DotDict(item, self.raise_error, self.convert_iterables))  # Pass convert_iterables flag
            else:
                result.append(item)
    
        if self.convert_iterables:
            return result  # Convert all iterables to lists
        else:
            # Preserve the original type of the iterable
            if isinstance(iterable, tuple):
                return tuple(result)
            elif isinstance(iterable, set):
                return set(result)
            return result  # Default to list for other iterables

    def __getattr__(self, str name):
        """Handle dynamic attribute access gracefully."""
        try:
            value = self.__dict__[name]
            if value is None and not self.raise_error:
                return NullDotDict()  # Return NullDotDict instead of None
            if isinstance(value, (list, tuple, set)):
                return self._wrap_iterable(value)
            return value
        except KeyError:
            if self.raise_error:
                raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
            return NullDotDict()  # Return NullDotDict for missing attributes

    def __setattr__(self, str name, value):
        """Allow dynamic assignment of attributes."""
        PyDict_SetItem(self.__dict__, name, self._wrap_value(value))

    def to_dict(self):
        """Convert the DotDict into a standard dictionary."""
        return self._convert_to_dict()

    cdef dict _convert_to_dict(self):
        """Recursively convert the DotDict into a standard dictionary."""
        cdef dict output = PyDict_New()
        cdef object key, value
        for key, value in self.__dict__.items():
            if isinstance(value, DotDict):
                PyDict_SetItem(output, key, value.to_dict())
            elif isinstance(value, (list, tuple, set)):
                PyDict_SetItem(output, key, self._convert_iterables(value))
            else:
                PyDict_SetItem(output, key, value)
        return output

    cdef object _convert_iterables(self, iterable):
        """Helper function to convert lists, tuples, and sets."""
        if isinstance(iterable, list):
            return self._wrap_iterable(iterable)
        elif isinstance(iterable, tuple):
            return self._wrap_iterable(iterable)
        elif isinstance(iterable, set):
            return self._wrap_iterable(iterable)
        return iterable


cdef class NullDotDict:
    """
    A proxy class to handle None values gracefully in Cython.
    Acts like a stand-in for None, but does not raise errors for attribute access.
    """

    def __getattr__(self, str name):
        """Always return itself for any attribute access."""
        return self

    def __call__(self, *args, **kwargs):
        """Support callable behavior, returning None."""
        return None

    def __repr__(self):
        """Provide a string representation for debugging."""
        return "NullDotDict(None)"

    def __bool__(self):
        """Behave like None in boolean context."""
        return False

    def __eq__(self, other):
        """Equality comparison with None or another NullDotDict."""
        return other is None or isinstance(other, NullDotDict)