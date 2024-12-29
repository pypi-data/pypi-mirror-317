from strath import ensure_path_is_str

from ._no_path_check import\
	sp_append_no_path_check,\
	sp_remove_no_path_check


class SysPathBundle:
	"""
	Upon instantiation, a bundle stores several paths and adds them to
	sys.path. When a bundle is cleared, it erases its content and removes it
	from sys.path. Thus, this class facilitates adding and removing a group of
	paths.

	This class is a context manager. If a bundle is used in a with statement as
	in the following example, it is cleared at the block's end.

	with SysPathBundle(("path/to/package1", "path/to/package2")):
	"""

	def __init__(self, content):
		"""
		The constructor needs the paths (type str or pathlib.Path) to store in
		this bundle and add to sys.path. If a path in argument content is
		None or is already in sys.path, the bundle will not store it.

		Args:
			content (generator, list, set or tuple): the paths to store in this
				bundle.

		Raises:
			TypeError: if a path is not None and not of type str or
				pathlib.Path.
		"""
		self._content = list()
		self._fill_content(content)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.clear()

	def clear(self):
		"""
		Erases this bundle's content and removes it from sys.path.
		"""
		while len(self._content) > 0:
			path = self._content.pop()
			sp_remove_no_path_check(path)

	def contains(self, some_path):
		"""
		Indicates whether this bundle cotains the given path.

		Args:
			some_path (str or pathlib.Path): the path whose presence is
				verified.

		Returns:
			bool: True if this bundle cotains the given path, False otherwise.

		Raises:
			TypeError: if a path is not None and not of type str or
				pathlib.Path.
		"""
		some_path = ensure_path_is_str(some_path, True)
		return some_path in self._content

	def _fill_content(self, content):
		for path in content:
			path = ensure_path_is_str(path, True)

			if sp_append_no_path_check(path):
				# Any path in self._content is a string.
				self._content.append(path)
