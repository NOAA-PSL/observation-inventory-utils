import yaml
import attr
import pathlib
from collections import defaultdict

def is_valid_yaml(instance, attribute, value):
    try:
        ext = pathlib.Path(value).suffix
    except Exception as e:
        raise ValueError(f'Invalid path: {value}, error: {e}')

    if ext != '.yaml' and ext != '.yml':
        raise TypeError(f'Not a recognized yaml extension: {ext}')


def is_expected_return_type(value, instance_type):

    actual_type = type(value)
    if not isinstance(value, instance_type):
        msg = f'Wrong instance type, expected: {instance_type}, found: ' \
              f'{actual_type}'
        raise ValueError(msg)

    return True


@attr.s(slots=True)
class YamlLoader(object):

    yaml_file = attr.ib(validator=is_valid_yaml)
    multiple_docs = attr.ib(
        validator=attr.validators.instance_of(bool), default=False)

    def load(self):
        print(f'multiple_docs: {self.multiple_docs}')
        try:
            print(f'loading yaml file: {self.yaml_file}')
            with open(self.yaml_file, 'r') as yaml_stream:
                documents = list(
                    yaml.load_all(yaml_stream, Loader=yaml.SafeLoader)
                )
                if (
                    self.multiple_docs == False and len(documents) > 1
                ) or (
                    len(documents) == 0
                ):
                    msg = f'Too many or too few documents loaded: loaded ' \
                          f'document count: {len(documents)}'
                    raise ValueError(msg)
        except yaml.YAMLError as e:
            raise TypeError(f'Cannot load yaml file: {self.yaml_file}, {e}')
        except OSError as e:
            msg = """ Please ensure the file exists and you have the required
                      access privileges."""
            raise VergeMLError(f"Could not open {self.yaml_file}: {e.strerror}", msg)
        except Exception as e:
            raise ValueError(f'Unkown error when parsing {self.yaml_file}, err: {e}')
        
        return documents


    def get_value(self, key, document, return_type, multiple_docs=False):
        """Lookup a key in a nested list of documents, return all matches"""
        
        found_keys = list(self._get_nested_key(key, document))

        print(f'values found: {found_keys}')
        
        if len(found_keys) > 1:
            msg = f'Key "{key}" found multiple times. Result ambiguous.'
            raise ValueError(msg)

        if len(found_keys) == 0:
            msg = f'Key "{key}" was not found in data: {document}.'
            raise ValueError(msg)
        value = is_expected_return_type(found_keys[0], return_type) 
        return found_keys[0]


    def _get_nested_key(self, key, document):
        if isinstance(document, list):
            for d in document:
                for result in self._get_nested_key(key, d):
                    yield result

        if isinstance(document, dict):
            for k, v in document.items():
                if key == k:
                    yield v
                if isinstance(v, dict):
                    for result in self._get_nested_key(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self._get_nested_key(key, d):
                            yield result
