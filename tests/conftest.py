import pytest

from legacy_api_testing import load_collection


@pytest.fixture(scope="session")
def collection():
    return load_collection()
