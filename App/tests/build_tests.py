import os, pytest

from datetime import timedelta
from unittest import mock

from App.controllers import create_app

# Define a fixture function that returns a mock config object
@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") != "true", reason="only run on GitHub Actions")
def mock_config():
    # Create a mock config object with some attributes
    config = mock.Mock()
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    config.SQLALCHEMY_DATABASE_URI = "host='localhost' dbname='sqlite' user='viewer'"
    config.SECRET_KEY = "123456789"

    return config

# Define a test function that uses the fixture as an argument
@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") != "true", reason="only run on GitHub Actions")
def test_app(mock_config):

    app = create_app(mock_config)
    assert app.config['JWT_ACCESS_TOKEN_EXPIRES'] == timedelta(days=1)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "host='localhost' dbname='sqlite' user='viewer'"
    assert app.config['SECRET_KEY'] == "123456789"