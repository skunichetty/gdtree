from typing import List
from gdtree.utils import MAX_DEPTH


class EndStateHistory:
    """
    A container that holds the end state history as encountered during traversal. An end state is a boolean values
    storeing if this entry exists as the last element in an lexicographical ordering
    of the directory tree. EndStateHistory is a container of these values for each level of the directory tree
    traversed for a given entry.
    """

    def __init__(self, input_history: List[bool] = None):
        """
        Initializes the EndStateHistory container.

        Args:
            input_history (List[bool], optional): An boolean list holding the sequential end state history.
            The order of the array is read from least depth in tree to greatest depth in tree. Defaults to None.

        Raises:
            ValueError: Raises if the input end state history list length exceeds the maximum allowed depth
        """
        self.history = 0
        self.depth = 0
        if input_history is not None and len(input_history) > 0:
            if len(input_history) > MAX_DEPTH:
                raise ValueError(
                    "Input list has too many values (greater than maximum allowed depth)"
                )
            self.depth = len(input_history)
            for index, state in enumerate(input_history):
                self.history |= state << index

    def __len__(self) -> int:
        """
        Gets the length of the history stored, corresponding to the depth of the traversal history up to that point.

        Returns:
            int: The length of this history
        """
        return self.depth

    def __getitem__(self, key: int) -> bool:
        """
        Gets the end state value at the given depth

        Args:
            key (int): The depth to retrieve the end state value at

        Raises:
            IndexError: Raises if the depth given exceeds the bounds of the history

        Returns:
            bool: The end state value at the depth given
        """
        if key >= self.depth or key < 0:
            raise IndexError("Index %d outside of history bounds" % key)
        mask = 1 << key
        return bool(self.history & mask)

    def __setitem__(self, key: int, value: bool) -> None:
        """
        Sets the end state value at the given index

        Args:
            key (int): The index to retrieve the end state value at
            value (bool): The end state value to set at the given index

        Raises:
            IndexError: Raises if the index given exceeds the length of the current instance
        """
        if key >= self.depth or key < 0:
            raise IndexError("Index %d outside of history bounds" % key)
        mask = 1 << key
        if value:
            self.history |= mask
        else:
            self.history &= ~mask

    def append(self, value: bool) -> None:
        """
        Appends new end state value to the current instance of EndStateHistory

        Args:
            value (bool): The new end state value to append

        Raises:
            DepthError: Raises if attempt is made to extend end state beyond maximum depth
        """
        if self.depth == MAX_DEPTH:
            raise DepthError(
                "Attempted to extend state history beyond maximum allowed traversal depth"
            )
        prev_depth = self.depth
        self.depth += 1
        self[prev_depth] = value

    def __iter__(self):
        """
        Returns an iterator to traverse the history

        Returns:
            _StateHistoryIterator: Iterator to iterate through this instance of EndStateHistory
        """
        return _StateHistoryIterator(self)

    def extend(self, other) -> None:
        """
        Extends this instance of EndStateHistory with the history from another. Appends the
        history values from the other history to the end of this instances container. The
        other instance is not mutated.

        Args:
            other (EndStateHistory): The other EndStateHistory whose values will be extended

        Raises:
            DepthError: Raises if extension by other history will exceed maximum allowed traversal depth
        """
        if (self.depth + other.depth) > MAX_DEPTH:
            raise DepthError(
                "Attempted to extend state history beyond maximum allowed traversal depth"
            )
        other_history = other.history
        other_history <<= self.depth
        self.history |= other_history
        self.depth += other.depth


class _StateHistoryIterator:
    """
    An iterator meant to iterate through EndStateHistory
    """

    def __init__(self, history: EndStateHistory):
        self.lim = 1 << len(history)
        self.mask = 1
        self.history = history.history

    def __iter__(self):
        return self

    def __next__(self):
        if self.mask < self.lim:
            temp = self.mask
            self.mask *= 2
            return bool(self.history & temp)
        else:
            raise StopIteration


class DepthError(Exception):
    """
    An error called when a DirectoryTreeEntry or traversal function attempts
    to exceed the maximum program depth
    """

    def __init__(self, message: str):
        self.message = message
