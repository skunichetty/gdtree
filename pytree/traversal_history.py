from typing import Tuple
import pytree.constants as constants


class TraversalHistory:
    """
    A class that holds the traversal history.
    """

    def __init__(self, history: int = -1, depth=0):
        self.history = history
        self.depth = depth

    def update_history(self, depth: int, value: bool):
        """
        Updates the history entry at the given depth

        Args:
            depth (int): The (zero-indexed) depth at which to update history.
            value (bool): The new value to change it to

        Raises:
            DepthError: Depth is negative or exceeds current depth
        """
        if depth < 0 or depth >= self.depth:
            raise DepthError(
                "Depth of %d exceeds current history depth" % depth
            )
        # KEY - the newest state resides at the MSB (bit at index $depth-1$)
        # This makes it easier to read the history values back (have to start from
        # LSB and move forward)
        mask = 1 << (depth)
        if value:
            self.history |= mask
        else:
            self.history &= ~mask

    def add_history(self, is_end: bool) -> Tuple[int, int]:
        """
        Adds a new history state entry to the history class

        Args:
            is_end (bool): The history state to append

        Raises:
            DepthError: Attempted to update history beyond max possible depth

        Returns:
            Tuple[int, int]: A tuple containing the new history and the new depth of this traversal
        """
        if self.depth == constants.MAX_DEPTH:
            raise DepthError(
                "Attempted to update history to extend beyond maximum allowed depth of %d"
                % constants.MAX_DEPTH
            )
        if self.depth == 0:
            self.history = 0
        if is_end:
            mask = 1 << self.depth
            self.history |= mask
        self.depth += 1
        return self.history, self.depth


class DepthError(Exception):
    """
    An error called when a DirectoryTreeEntry or traversal function attempts
    to exceed the maximum program depth
    """

    def __init__(self, message: str):
        self.message = message
