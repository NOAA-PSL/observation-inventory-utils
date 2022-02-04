"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
import os
import pathlib
import pytest
from obs_inv_utils import yaml_utils as yu


YAML_CONFIGS_PATH = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'yaml_configs'
)

YAML_BAD_SUFFIX = os.path.join(YAML_CONFIGS_PATH, 'bad_suffix.txt')
YAML_BAD_FORMAT1 = os.path.join(YAML_CONFIGS_PATH, 'invalid_format1.yaml')
YAML_BAD_FORMAT2 = os.path.join(YAML_CONFIGS_PATH, 'invalid_format2.yaml')
YAML_BAD_FORMAT3 = os.path.join(YAML_CONFIGS_PATH, 'invalid_format3.yaml')
YAML_ATMOS_1P0_COUPLED = os.path.join(YAML_CONFIGS_PATH, 'atmos.1p0.coupled.yaml')
YAML_MULTIPLE_DOCS = os.path.join(YAML_CONFIGS_PATH, 'multiple_documents.yaml')

def test_is_invalid_yaml__invalid_suffix():
    """
    Test the 'is_invalid_yaml' validator with .txt suffix
    """

    with pytest.raises(TypeError):
        yaml_loader = yu.YamlLoader(YAML_BAD_SUFFIX)


def test_is_invalid_yaml__invalid_path():
    """
    Test the 'is_invalid_yaml' validator with .txt suffix
    """

    with pytest.raises(ValueError):
        yaml_loader = yu.YamlLoader({})



def test_load__invalid_format():
    """
    Test the 'is_invalid_yaml' validator with .txt suffix
    """

    with pytest.raises(TypeError):
        yl = yu.YamlLoader(YAML_BAD_FORMAT1)
        documents = yl.load()
        print(f'documents: {documents}')	

    with pytest.raises(TypeError):
        yl = yu.YamlLoader(YAML_BAD_FORMAT2)
        documents = yl.load()
        print(f'documents: {documents}')

    with pytest.raises(TypeError):
        yl = yu.YamlLoader(YAML_BAD_FORMAT3)
        documents = yl.load()
        print(f'documents: {documents}')


def test_load__valid_format():
    yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)

    try:
        document = yl.load()
        print(f'document: {document}')
    except Exception as e:
        msg = f'"test_YamlLoader__valid_format raised exception {e}'
        assert False, msg


def test_get_value__multiple_documents():
    try:
        yl = yu.YamlLoader(YAML_MULTIPLE_DOCS, True)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('a', documents, int)
    except Exception as e:
        msg = f'Unexpected exception parsing yaml with multiple documents: {e}'
        assert False, msg

    with pytest.raises(ValueError):
        yl = yu.YamlLoader(YAML_MULTIPLE_DOCS, False)
        documents = yl.load()


def test_get_value__value_not_found():
    with pytest.raises(ValueError):
        yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('blah', documents, dict)


def test_get_value__dict_val_found():
    try:
        yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('atmos_general', documents, dict)
    except Exception as e:
        msg = f'Unexpected exception parsing yaml with multiple documents: {e}'
        assert False, msg

    with pytest.raises(ValueError):
        yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('niter', documents, dict)


def test_get_value__key_found_multiple_times():
    with pytest.raises(ValueError):
        yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('resolution', documents, str)


def test_get_value__bool_val_found():
    try:
        yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('funky_bool', documents, bool)
    except Exception as e:
        msg = f'Unexpected exception parsing yaml with multiple documents: {e}'
        assert False, msg

    with pytest.raises(ValueError):
        yl = yu.YamlLoader(YAML_ATMOS_1P0_COUPLED)
        documents = yl.load()
        print(f'documents: {documents}')
        yl.get_value('niter', documents, bool)
