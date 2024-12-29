import sys


def sp_append_no_path_check(some_path):
	was_path_appended = False

	if some_path not in sys.path and some_path is not None:
		sys.path.append(some_path)
		was_path_appended = True

	return was_path_appended


def sp_remove_no_path_check(some_path):
	was_path_removed = False

	try:
		sys.path.remove(some_path) # ValueError if argument not in list
		was_path_removed = True
	except ValueError:
		pass

	return was_path_removed
