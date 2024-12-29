import sys

from strath import ensure_path_is_str

from ._no_path_check import\
	sp_append_no_path_check,\
	sp_remove_no_path_check


def sp_append(some_path):
	"""
	Appends the given path to the end of list sys.path if it does not already
	contain the path. If the path is of type pathlib.Path, it is converted to a
	string. If the path is None, this method does not change sys.path.

	Args:
		some_path (str or pathlib.Path): the path to append to sys.path.

	Returns:
		bool: True if some_path was appended to sys.path, False otherwise.

	Throws:
		TypeError: if argument some_path is not None and it is not an instance
			of str or pathlib.Path.
	"""
	some_path = ensure_path_is_str(some_path, True)
	return sp_append_no_path_check(some_path)


def sp_contains(some_path):
	"""
	Indicates whether list sys.path contains the given path.

	Args:
		some_path (str or pathlib.Path): the path whose presence is verified.

	Returns:
		bool: True if sys.path contains argument some_path, False otherwise.

	Throws:
		TypeError: if argument some_path is not None and it is not an instance
			of str or pathlib.Path.
	"""
	some_path = ensure_path_is_str(some_path, True)
	return some_path in sys.path


def sp_remove(some_path):
	"""
	Removes the given path from list sys.path if it contains the path.

	Args:
		some_path (str or pathlib.Path): the path to remove from sys.path.

	Returns:
		bool: True if some_path was removed from sys.path, False otherwise.

	Throws:
		TypeError: if argument some_path is not None and it is not an instance
			of str or pathlib.Path.
	"""
	some_path = ensure_path_is_str(some_path, True)
	return sp_remove_no_path_check(some_path)
