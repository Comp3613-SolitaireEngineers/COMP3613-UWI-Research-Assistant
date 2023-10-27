# This code is used to prevent the build test on GitHub from failing due to the 
# gitignored custom_config.py file

import os, pytest

from datetime import timedelta
from unittest import mock

from App.controllers import create_app

@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") != "true", reason="only run on GitHub Actions - build tests")
def test_mock_config():
    # Create a mock config object with the attributes from custom_config
    config = mock.Mock()
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    config.SQLALCHEMY_DATABASE_URI = "host='localhost' dbname='sqlite' user='viewer'"
    config.SECRET_KEY = "123"

    return config

# This code is used to prevent the build test on GitHub from failing due to the gitignored custom_config.py file
@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") != "true", reason="only run on GitHub Actions - build tests")
def test_app(mock_config):

    app = create_app(mock_config)
    assert app.config['JWT_ACCESS_TOKEN_EXPIRES'] == timedelta(days=1)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "host='localhost' dbname='sqlite' user='viewer'"
    assert app.config['SECRET_KEY'] == "123"