from pathlib import Path
import sys

from strath import ensure_path_is_str


_INIT_SYS_PATH = list(sys.path)

_LOCAL_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _LOCAL_DIR.parent
_LIB_DIR = _REPO_ROOT/"syspathmodif"


def _reset_sys_path():
	# Copying the list is necessary to preserve the initial state.
	sys.path = list(_INIT_SYS_PATH)


sys.path.append(str(_REPO_ROOT))
from syspathmodif import SysPathBundle
_reset_sys_path()


def assert_path_in_sys_path(some_path, is_in_sys_path):
	some_path = ensure_path_is_str(some_path, True)
	assert (some_path in sys.path) == is_in_sys_path


def assert_path_is_present(some_path, bundle, is_in_sys_path, is_in_bundle):
	some_path = ensure_path_is_str(some_path, True)
	assert (some_path in sys.path) == is_in_sys_path
	assert bundle.contains(some_path) == is_in_bundle


def generate_paths():
	yield _LOCAL_DIR
	yield _REPO_ROOT
	yield _LIB_DIR


def test_init_generator():
	try:
		from inspect import isgenerator

		content_gen = generate_paths()
		assert isgenerator(content_gen)
		bundle = SysPathBundle(content_gen)

		assert_path_is_present(_LOCAL_DIR, bundle, True, False)
		assert_path_is_present(_REPO_ROOT, bundle, True, True)
		assert_path_is_present(_LIB_DIR, bundle, True, True)

	finally:
		_reset_sys_path()


def test_init_list():
	try:
		content = [_LOCAL_DIR, _REPO_ROOT, _LIB_DIR]
		assert isinstance(content, list)
		bundle = SysPathBundle(content)

		assert_path_is_present(_LOCAL_DIR, bundle, True, False)
		assert_path_is_present(_REPO_ROOT, bundle, True, True)
		assert_path_is_present(_LIB_DIR, bundle, True, True)

	finally:
		_reset_sys_path()


def test_init_tuple():
	try:
		content = (_LOCAL_DIR, _REPO_ROOT, _LIB_DIR)
		assert isinstance(content, tuple)
		bundle = SysPathBundle(content)

		assert_path_is_present(_LOCAL_DIR, bundle, True, False)
		assert_path_is_present(_REPO_ROOT, bundle, True, True)
		assert_path_is_present(_LIB_DIR, bundle, True, True)

	finally:
		_reset_sys_path()


def test_init_set():
	try:
		content = {_LOCAL_DIR, _REPO_ROOT, _LIB_DIR}
		assert isinstance(content, set)
		bundle = SysPathBundle(content)

		assert_path_is_present(_LOCAL_DIR, bundle, True, False)
		assert_path_is_present(_REPO_ROOT, bundle, True, True)
		assert_path_is_present(_LIB_DIR, bundle, True, True)

	finally:
		_reset_sys_path()


def test_clear():
	try:
		bundle = SysPathBundle((_LOCAL_DIR, _REPO_ROOT, _LIB_DIR))
		bundle.clear()

		assert_path_is_present(_LOCAL_DIR, bundle, True, False)
		assert_path_is_present(_REPO_ROOT, bundle, False, False)
		assert_path_is_present(_LIB_DIR, bundle, False, False)

		assert sys.path == _INIT_SYS_PATH

	finally:
		_reset_sys_path()


def test_context_management():
	try:
		with SysPathBundle((_LOCAL_DIR, _REPO_ROOT, _LIB_DIR)) as bundle:
			assert_path_is_present(_LOCAL_DIR, bundle, True, False)
			assert_path_is_present(_REPO_ROOT, bundle, True, True)
			assert_path_is_present(_LIB_DIR, bundle, True, True)

		assert_path_in_sys_path(_LOCAL_DIR, True)
		assert_path_in_sys_path(_REPO_ROOT, False)
		assert_path_in_sys_path(_LIB_DIR, False)

		assert sys.path == _INIT_SYS_PATH

	finally:
		_reset_sys_path()
