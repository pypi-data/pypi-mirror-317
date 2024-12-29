import pytest

from pathlib import Path
import sys


# The syspathmodif's modules are not supposed to be directly used out of their
# package. These tests ensure that the wildcard import does not include them.

# Since wildcard imports are not allowed within classes and functions,
# the tests perform them with exec.


_REPO_ROOT = str(Path(__file__).resolve().parents[1])


def test_module_import_syspathmodif():
	sys.path.append(_REPO_ROOT)
	exec("from syspathmodif import *")
	sys.path.remove(_REPO_ROOT)

	with pytest.raises(NameError, match=".*_no_path_check.*"):
		_no_path_check

	with pytest.raises(NameError, match=".*_syspathbundle.*"):
		_syspathbundle

	with pytest.raises(NameError, match=".*_syspathmodif.*"):
		_syspathmodif
