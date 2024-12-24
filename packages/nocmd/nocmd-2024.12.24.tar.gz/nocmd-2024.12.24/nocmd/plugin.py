import pytest

from nocmd import Cmd
from nocmd import RemoteCmd


@pytest.fixture(scope="session")
def cmd():
    return Cmd


@pytest.fixture(scope="session")
def remote_cmd():
    return RemoteCmd
