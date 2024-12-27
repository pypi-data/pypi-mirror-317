import pytest

from python_plugins.utils import remove_pycache
from python_plugins.utils import remove_ipynb_checkpoints

@pytest.mark.skip
def test_remove_pycache():
    remove_pycache("./tests")

@pytest.mark.skip()
def test_remove_pycache():
    remove_pycache()
