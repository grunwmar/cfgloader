import _io
import os
import json
import toml
import yaml
import configparser
import requests

from ._dotdict import _DotDict

yaml.load_custom = yaml.safe_load
yaml.loads_custom = yaml.safe_load

json.load_custom = json.load
json.loads_custom = json.loads

toml.load_custom = toml.load
toml.loads_custom = toml.loads


TO_STRING_INDENT = 3
TO_STRING_ENSURE_ASCII = False

FORMAT_JSON = "json"
FORMAT_YAML = "yaml"
FORMAT_TOML = "toml"


def _all_none(*args):
    return not any(args)


def _to_dict_iter(dct):
    new_dict = dict()
    for key, value in dct.items():
        if hasattr(value, 'keys'):
            value = dict(value)
        new_dict[key] = value
    return new_dict


class DeserializerDict(dict):
    """ Class designed to quick and easy access to configuration files. """

    @classmethod
    def load(cls, file=None, string=None, http_url=None, http_args=None, sformat=None, default_content=None):

        content = default_content if default_content is not None else {}

        def load_(module):
            def inner(obj):
                if isinstance(obj, _io.TextIOWrapper):
                    return module.load_custom(obj)
                elif isinstance(obj, str):
                    return module.loads_custom(obj)
            return inner

        def load_ini(obj):
            config = configparser.ConfigParser()
            if isinstance(obj, _io.TextIOWrapper):
                config.read_string(obj.read())
                new_dict = _to_dict_iter(config)
                return new_dict

        method = {
                ".json": load_(json),
                ".yaml": load_(yaml),
                ".toml": load_(toml),
                ".ini": load_ini
            }

        if _all_none(http_url, string, sformat) and isinstance(file, str):
            with open(file, "r") as fp:
                _, ext = os.path.splitext(file)
                content.update(method[ext](fp))

        elif _all_none(http_url, string, sformat) and isinstance(file, _io.TextIOWrapper):
            _, ext = os.path.splitext(file.name)
            content.update(method[ext](file))

        elif _all_none(http_url) and isinstance(string, str) and isinstance(sformat, str):
            content.update(method[f".{sformat}"](string))

        elif _all_none(string) and isinstance(http_url, str) and isinstance(sformat, str):

            if http_args is None:
                get = requests.get(http_url)
            else:
                get = requests.get(http_url, *http_args)

            if get.status_code == 200:
                content.update(method[f".{sformat}"](get.text))
        else:
            raise ValueError("Invalid combination of input parameters.")

        return cls(content)

    @classmethod
    def from_http(cls, url: str, sformat: str, default_content=None, args: dict = None):
        return cls.load(http_url=url, http_args=args, sformat=sformat, default_content=default_content)

    @classmethod
    def from_string(cls, string: str, sformat: str, default_content=None):
        return cls.load(string=string, sformat=sformat, default_content=default_content)

    @classmethod
    def from_file(cls, file, default_content=None):
        return cls.load(file=file, default_content=default_content)

    def __init__(self, dict_):
        super().__init__(dict_)

    def __getitem__(self, items):
        """ Override original __getitem__ method to be able to accept more arguments """

        result = dict(self)
        for i in items:
            if isinstance(result, list) or isinstance(result, tuple):
                key = int(i)
            else:
                key = i
                if len(key) == 0:
                    continue
            result = result[key]
        return result

    def __call__(self, dot_dict=True):
        if dot_dict:
            return _DotDict(self)
        else:
            return _to_dict_iter(self)

    def __str__(self):
        json_formatted = json.dumps(_DotDict(self), ensure_ascii=TO_STRING_ENSURE_ASCII, indent=TO_STRING_INDENT)
        return f"{self.__class__.__name__}({json_formatted})"
