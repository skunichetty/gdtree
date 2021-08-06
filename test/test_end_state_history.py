from unittest import TestCase, main
from gdtree.utils import MAX_DEPTH
from gdtree.end_state_history import DepthError, EndStateHistory


class TestEndStateHistory(TestCase):
    def test_construction_default_length(self):
        """
        Tests that default construction produces the correct depth
        """
        entry = EndStateHistory()
        self.assertEqual(len(entry), 0)

    def test_construction_length_error(self):
        """
        Tests that the length of the input boolean array does not exceed
        maximum allowed depth
        """
        history = [False] * (MAX_DEPTH + 1)
        with self.assertRaises(ValueError):
            entry = EndStateHistory(history)

    def test_construction_empty_input_length(self):
        """
        Tests that an empty input array will correctly process length
        """
        entry = EndStateHistory([])
        self.assertEqual(len(entry), 0)

    def test_len_empty(self):
        """
        Tests that the history length is 0 when no values are added
        """
        entry = EndStateHistory()
        self.assertEqual(len(entry), 0)

    def test_len_nonempty(self):
        """
        Tests that the history length is properly returned when no values are added
        """
        history = [True, False, True, True, False, False, False]
        entry = EndStateHistory(history)
        self.assertEqual(len(entry), 7)

    def test_len_max_length(self):
        """
        Tests that the history length is properly returned at maximum depth
        """
        history = [False] * MAX_DEPTH
        entry = EndStateHistory(history)
        self.assertEqual(len(entry), MAX_DEPTH)

    def test_history_append_length(self):
        """
        Tests that adding a new value to history increases history length
        """
        entry = EndStateHistory([True, False, True, False, False, True])
        entry.append(True)
        self.assertEqual(len(entry), 7)

    def test_history_append_length(self):
        """
        Tests that adding a new value to history adds a new value to the end
        """
        entry = EndStateHistory([True, False, True, False, False, True])
        entry.append(False)
        self.assertFalse(entry[6])

    def test_history_append_error(self):
        """
        Tests that an error is raised when trying to update history
        past the max possible depth
        """
        entry = EndStateHistory([False] * MAX_DEPTH)
        with self.assertRaises(DepthError):
            entry.append(True)

    def test_history_append_start(self):
        """
        Tests that a new value is successfully added at the start
        """
        entry = EndStateHistory()
        entry.append(True)
        self.assertTrue(entry[0])

    def test_iteration(self):
        """
        Tests that history is iterated through in the correct order
        """
        history = [True, False, True, True, False]
        entry = EndStateHistory(history)
        for value, expected_value in zip(entry, history):
            self.assertEqual(value, expected_value)
        for value in entry:
            print(value)

    def test_access(self):
        """
        Tests that history can be easily accessed
        """
        entry = EndStateHistory([True, False, True, False, False, True])
        self.assertFalse(entry[3])
        self.assertTrue(entry[2])

    def test_access_error(self):
        """
        Tests that an error is thrown when accessing an invalid index
        """
        entry = EndStateHistory([True, False, True, False, False, True])
        with self.assertRaises(IndexError):
            self.assertTrue(entry[6])

    def test_mutate(self):
        """
        Tests that history can be easily mutated
        """
        entry = EndStateHistory([True, False, True, False, False, True])
        self.assertTrue(entry[0])
        entry[0] = False
        self.assertFalse(entry[0])

    def test_mutate_error(self):
        """
        Tests that an error is thrown when accessing an invalid index
        """
        entry = EndStateHistory([True, False, True, False, False, True])
        with self.assertRaises(IndexError):
            entry[6] = True

    def test_extend(self):
        """
        Tests that the history can be extended with another history
        """
        entry_one = EndStateHistory([True, False, True])
        entry_two = EndStateHistory([False, False, True])
        output_values = [True, False, True, False, False, True]
        entry_one.extend(entry_two)
        for state, expected_output in zip(entry_one, output_values):
            self.assertEqual(state, expected_output)

    def test_extend_error(self):
        """
        Tests that a depth error is raised when attempting to extend
        one history past the maximum depth
        """
        entry_one = EndStateHistory([False] * MAX_DEPTH)
        entry_two = EndStateHistory([False, False, True])
        with self.assertRaises(DepthError):
            entry_one.extend(entry_two)

    def test_extend_error_edge(self):
        """
        Tests that a depth error is raised when attempting to extend
        one history exactly one past the maximum depth
        """
        entry_one = EndStateHistory([False] * (MAX_DEPTH - 2))
        entry_two = EndStateHistory([False, False, True])
        with self.assertRaises(DepthError):
            entry_one.extend(entry_two)

    def test_extend_empty(self):
        """
        Tests that a history can be extended from empty values without any issue
        """
        entry_one = EndStateHistory()
        entry_two = EndStateHistory([False, False, True])
        output_values = [False, False, True]
        entry_one.extend(entry_two)
        for state, expected_output in zip(entry_one, output_values):
            self.assertEqual(state, expected_output)

    def test_extend_no_change(self):
        """
        Tests that extending a history from one instance does not change the values of the other instance.
        """
        entry_one = EndStateHistory([True, False, True])
        entry_two = EndStateHistory([False, False, True])
        output_values = [False, False, True]
        entry_one.extend(entry_two)
        for state, expected_output in zip(entry_two, output_values):
            self.assertEqual(state, expected_output)

    def test_extend_depth_change(self):
        """
        Tests that extending a history increments depth properly
        """
        entry_one = EndStateHistory([True, False, True])
        entry_two = EndStateHistory([False, False, True])
        entry_one.extend(entry_two)
        self.assertEqual(len(entry_one), 6)


if __name__ == "__main__":
    main()
