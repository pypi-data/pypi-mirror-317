"""This module holds classes and functions related to heaps and priority queues.

This module contains `PriorityQueue`, an implementation of a priority queue, and `PriorityQueueUnderflowError`, an error
raised by `PriorityQueue`. This module also contains the function `build_min_heap` which modifies the elements of an
`dalpy.arrays.Array` so that they construct a min heap.

Examples:
    Initializing, adding, and removing elements from a `PriorityQueue`:

        q = PriorityQueue()
        q.insert('a', 2)
        q.insert('b', 1)
        q.extract_min()

    The following code will raise a `PriorityQueueUnderflowError` because the second extract min is done on an empty
    `PriorityQueue`:

        q.extract_min()
        q.extract_min()
"""

from dalpy.arrays import Array
from heapq import heapify


class PriorityQueueUnderflowError(Exception):
    """This class is used by `PriorityQueue` to raise errors for operations done on an empty `PriorityQueue`."""

    def __init__(self, operation):
        """Initializes a `PriorityQueueUnderflowError` that will be raised associated with a `PriorityQueue` operation.

        Args:
            operation: a string specifying the operation to raise an error on
        """
        super().__init__(f'Cannot perform {operation} on an empty priority queue.')


class PriorityQueue:
    """This class represents a minimum priority queue.

    One may assume that this `PriorityQueue` has no maximum capacity.

    Examples:
        To initialize a `PriorityQueue`:

            q = PriorityQueue()

        To add elements to `q`:

            q.insert('a', 2)
            q.insert('b', 1)

        To remove and return the minimum priority element of `q` (in this case `x = 'b'`):

            x = q.extract_min()

        To see the minimum priority element of `q` (in this case `y = 'a'`):

            y = q.front()

        To decrease the priority of an element in `q`:

            q.decrease_key('a', 0)
    """

    def __init__(self):
        """Initializes an empty `PriorityQueue` in `O(1)` time."""
        self.__buf = list()
        self.__indices = dict()

    def insert(self, element, priority):
        """Inserts an element into the `PriorityQueue` with an associated priority.

        This operation runs in `O(log(n))` time where `n` is the size of this `Queue`.

        Args:
            element: An element to add to this `PriorityQueue`. This can be of any type.
            priority: The integer priority `element` should have in this `PriorityQueue`.
        """
        if element in self.__indices:
            raise ValueError(f'{element} already is in the PriorityQueue, to decrease its priority, use decrease_key()')
        # adding new item to end of list, usually O(1), could degrade to O(n) if resize needed but resizes will have to
        # happen regardless using any array-like structure to back a heap
        self.__buf.append((priority, element))
        # add new element as an entry into indices map (needed before _heapify_up which uses _swap which uses the map)
        self.__indices[element] = len(self.__buf) - 1
        self._heapify_up(len(self.__buf) - 1)

    def extract_min(self):
        """Removes the minimum priority element of this `PriorityQueue`.

        This operation runs in `O(log(n))` time where `n` is the size of this `PriorityQueue`.

        Returns:
            The element with the minimum priority in this `PriorityQueue`.

        Raises:
             PriorityQueueUnderflowError: If this `PriorityQueue` is empty.
        """
        if len(self.__buf) == 0:
            raise PriorityQueueUnderflowError('extract_min()')
        # after swapping min element with bottom heap element, immediately remove it from heap so that it is not
        # part of the _heapify_down. note that pop(-1) on list is O(1)
        self._swap(0, len(self.__buf) - 1)
        out = self.__buf.pop(-1)[1]
        self.__indices.pop(out)
        self._heapify_down(0)
        return out

    def minimum(self):
        """Gets the minimum priority element of this `PriorityQueue`.

        This operation runs in `O(1)` time with respect to the size of this `PriorityQueue`.

        Returns:
            The element with the minimum priority in this `PriorityQueue`.

        Raises:
             PriorityQueueUnderflowError: If this `PriorityQueue` is empty.
        """
        if len(self.__buf) == 0:
            raise PriorityQueueUnderflowError('minimum()')
        return self.__buf[0][1]

    def decrease_key(self, element, new_priority):
        """Decreases the priority of an element in this `PriorityQueue`.

        This operation runs in `O(log(n))` time where `n` is the size of this `PriorityQueue`.

        Args:
            element: The element whose priority is being updated.
            new_priority: The new priority of `element`. It should be `<=` its existing priority.

        Raises:
            ValueError: If `element` is not in this `PriorityQueue` or `new_priority` is greater than the existing
                        priority of `element`.
        """
        if element not in self.__indices:
            raise ValueError(f'{element} is not in PriorityQueue, it must be inserted with insert()')
        idx = self.__indices[element]
        if new_priority > self.__buf[idx][0]:
            raise ValueError(
                f'{element} has priority {self.__buf[idx][0]} < new_priority = {new_priority} (not a decrease)')
        self.__buf[idx] = (new_priority, element)
        self._heapify_up(idx)

    def size(self):
        """Returns the size of this `PriorityQueue` in `O(1)` time w/r/t the size of this `PriorityQueue`.

        Returns:
            The integer number of elements in this `PriorityQueue`.
        """
        return len(self.__buf)

    def is_empty(self):
        """Returns whether this `PriorityQueue` is empty in `O(1)` time w/r/t the size of this `PriorityQueue`.

        Returns:
            `True` if this `PriorityQueue` is empty, `False` otherwise.
        """
        return len(self.__buf) == 0

    # private class, instance methods

    @staticmethod
    def _parent(i):
        return int((i - 1) / 2)

    def _swap(self, i, j):
        tmp = self.__buf[i]
        self.__indices[self.__buf[i][1]] = j
        self.__buf[i] = self.__buf[j]
        self.__indices[self.__buf[j][1]] = i
        self.__buf[j] = tmp

    def _heapify_up(self, i):
        while i > 0 and self.__buf[i][0] < self.__buf[PriorityQueue._parent(i)][0]:
            self._swap(i, PriorityQueue._parent(i))
            i = PriorityQueue._parent(i)

    def _heapify_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < len(self.__buf) and self.__buf[left][0] < self.__buf[i][0]:
            smallest = left
        if right < len(self.__buf) and self.__buf[right][0] < self.__buf[smallest][0]:
            smallest = right
        if smallest != i:
            self._swap(smallest, i)
            self._heapify_down(smallest)


def build_min_heap(arr):
    """Modifies an `dalpy.arrays.Array` so that its elements make up a min heap.

    This method does not return a copy of the provided `dalpy.arrays.Array` whose elements make up a heap, it modifies
    it in place. Furthermore, all the elements (starting from index 0) are in a min heap. This method runs in `O(n)`
    time where `n` is the length of the input `dalpy.arrays.Array`.

    Args:
        arr: The input `dalpy.arrays.Array`. Its elements should be comparable with `<`, `>=`, etc.

    Raises:
        TypeError: If `arr` is not an `dalpy.arrays.Array`'.
    """
    if not isinstance(arr, Array):
        raise TypeError('can only build min heap of an Array')
    ls = [arr[i] for i in range(arr.length())]
    heapify(ls)
    for i in range(arr.length()):
        arr[i] = ls[i]
