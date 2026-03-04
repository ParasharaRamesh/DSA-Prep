from sortedcontainers import SortedList, SortedDict
from sortedcollections import ValueSortedDict

#option 1 using sorted collections 

value_sorted_dict = ValueSortedDict()
value_sorted_dict[1] = 3
value_sorted_dict[2] = 2
value_sorted_dict[3] = 1
print(value_sorted_dict)

# option 2 custom implementation
class ValueSortedDict:
    """
    A dictionary that maintains its items sorted by value.
    Values may be duplicated; keys are unique.
    All operations that modify the dictionary are O(log n) in the number of items,
    and lookups by key are O(1).

    The sorted order is maintained by a SortedDict that maps each value
    to a SortedList of keys having that value.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the dictionary. Accepts the same arguments as the built-in dict:
        - a mapping (e.g., another dict)
        - an iterable of (key, value) pairs
        - keyword arguments
        """
        self._map = {}                # key -> value
        self._values = SortedDict()   # value -> SortedList of keys
        # Populate from the given arguments
        if args or kwargs:
            # First positional argument may be a dict or an iterable of pairs
            if len(args) == 1:
                arg = args[0]
                if isinstance(arg, dict):
                    items = arg.items()
                else:
                    # Assume it's an iterable of (key, value) pairs
                    items = arg
                for key, value in items:
                    self[key] = value
            # Add any keyword arguments (keys must be strings, but that's fine)
            for key, value in kwargs.items():
                self[key] = value

    def __setitem__(self, key, value):
        """Insert or update key with the given value."""
        # If key already exists, remove it from its old value's key list
        if key in self._map:
            old_val = self._map[key]
            if old_val == value:
                return  # no change
            keys_for_val = self._values[old_val]
            keys_for_val.remove(key)          # O(log n)
            if not keys_for_val:               # if list becomes empty, delete the entry
                del self._values[old_val]      # O(log n)

        # Store the new mapping
        self._map[key] = value
        # Insert key into the list for the new value
        if value not in self._values:
            self._values[value] = SortedList()
        self._values[value].add(key)           # O(log n)

    def __delitem__(self, key):
        """Remove key from the dictionary. Raises KeyError if key not found."""
        value = self._map.pop(key)             # O(1) average; raises KeyError if missing
        keys_for_val = self._values[value]
        keys_for_val.remove(key)                # O(log n)
        if not keys_for_val:
            del self._values[value]             # O(log n)

    def __getitem__(self, key):
        """Return the value for key. Raises KeyError if key not found."""
        return self._map[key]

    def get(self, key, default=None):
        """
        Return the value for key if key exists, else default.
        This method never raises a KeyError.
        """
        return self._map.get(key, default)

    def pop(self, key, default=None):
        """
        If key exists, remove it and return its value.
        If key does not exist, return default if provided; otherwise raise KeyError.
        """
        if key in self._map:
            value = self._map[key]
            del self[key]          # O(log n) – uses __delitem__
            return value
        if default is not None:
            return default
        raise KeyError(key)

    def __contains__(self, key):
        """Return True if key is in the dictionary."""
        return key in self._map

    def __len__(self):
        """Return the number of items in the dictionary."""
        return len(self._map)

    def __iter__(self):
        """
        Iterate over keys in ascending order of their associated values.
        (If two keys have the same value, their relative order is the order of insertion,
        but they will always appear consecutively.)
        """
        for _, keys in self._values.items():
            for key in keys:
                yield key

    def items(self):
        """
        Iterate over (key, value) pairs in ascending order of value.
        """
        for value, keys in self._values.items():
            for key in keys:
                yield key, value

    def keys(self):
        """
        Iterate over keys in ascending order of value.
        """
        return iter(self)

    def values(self):
        """
        Iterate over values in ascending order, repeating each value for each key
        that has that value.
        """
        for value, keys in self._values.items():
            for _ in keys:
                yield value

    def __repr__(self):
        """Return a string representation similar to a regular dict."""
        items = list(self.items())
        return f"{self.__class__.__name__}({items!r})"

    # Optional: implement other dict-like methods for completeness
    def clear(self):
        """Remove all items."""
        self._map.clear()
        self._values.clear()

    def copy(self):
        """Return a shallow copy of the dictionary."""
        new = ValueSortedDict()
        new._map = self._map.copy()
        # Deep copy the sorted structure to preserve independent lists
        new._values = SortedDict()
        for value, keys in self._values.items():
            new._values[value] = SortedList(keys)
        return new

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """
        Create a new ValueSortedDict with keys from iterable and values set to value.
        """
        d = cls()
        for key in iterable:
            d[key] = value
        return d