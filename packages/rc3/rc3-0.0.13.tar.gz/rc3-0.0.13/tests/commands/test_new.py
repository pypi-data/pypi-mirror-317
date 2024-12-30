import os
import re

import pytest

from rc3 import cli
from rc3.common import json_helper, config_helper
from rc3.common.data_helper import SETTINGS_FILENAME, COLLECTION_FILENAME, GLOBAL_ENV_FILENAME, KEYRING_FILENAME


def test_new_from_empty(clean_home, clean_empty, runner):
    # pre-test RC_HOME doesn't exist
    rc_home = os.path.join(clean_home, '.rc')
    assert not os.path.exists(rc_home)

    # change to empty dir, and run init
    os.chdir(clean_empty)
    result = runner.invoke(cli.cli, ['new'], input='example-collection\n\n')
    assert result.exit_code == 0

    # test it exists now AND has rc files
    assert os.path.exists(rc_home)
    assert os.listdir(rc_home) == [GLOBAL_ENV_FILENAME, KEYRING_FILENAME, SETTINGS_FILENAME]
    assert os.listdir(clean_empty) == ['environments',
                                       'examples',
                                       'greetings-basic',
                                       'greetings-oauth2',
                                       COLLECTION_FILENAME]
    settings = json_helper.read_settings()
    assert settings.get('current_collection') == "example-collection"


def test_new_from_empty_no_examples(clean_home, clean_empty, runner):
    # pre-test RC_HOME doesn't exist
    rc_home = os.path.join(clean_home, '.rc')
    assert not os.path.exists(rc_home)

    # change to empty dir, and run init
    os.chdir(clean_empty)
    result = runner.invoke(cli.cli, ['new'], input='example-collection\nN\n')
    assert result.exit_code == 0

    # test it exists now AND has rc files
    assert os.path.exists(rc_home)
    assert os.listdir(rc_home) == [GLOBAL_ENV_FILENAME, KEYRING_FILENAME, SETTINGS_FILENAME]
    # should not have examples, since we said 'N' on input
    assert os.listdir(clean_empty) == ['environments',
                                       # 'examples',
                                       # 'greetings-basic',
                                       # 'greetings-oauth2',
                                       COLLECTION_FILENAME]
    settings = json_helper.read_settings()
    assert settings.get('current_collection') == "example-collection"


def test_new_from_existing(example_collection, runner):
    # CWD will be the example collection created
    result = runner.invoke(cli.cli, ['new'], input='example-collection\n\n')
    assert result.exit_code == 1
    # non-empty causes this msg
    assert "CWD must be empty to create a new collection" in result.output
    # existing collection.json causes this msg also
    assert "Try 'rc import' to import an existing" in result.output


def test_new_from_NOT_empty(clean_home, clean_empty, runner):
    # pre-test RC_HOME doesn't exist
    rc_home = os.path.join(clean_home, '.rc')
    assert not os.path.exists(rc_home)

    # change to empty dir, create tempfile
    # and then run new
    os.chdir(clean_empty)
    json_helper.write_json("temp.json",{})
    result = runner.invoke(cli.cli, ['new'], input='example-collection\n\n')
    assert result.exit_code == 1

    # test that we DO STILL init RC_HOME
    assert os.path.exists(rc_home)
    assert os.listdir(rc_home) == [GLOBAL_ENV_FILENAME, KEYRING_FILENAME, SETTINGS_FILENAME]
    # BUT we DON'T init the CWD, or import a collection
    assert os.listdir(clean_empty) == ['temp.json']
    settings = json_helper.read_settings()
    assert settings.get('current_collection') == ""

