import os
import re
from typing import TypeVar, Union

T = TypeVar("T", int, str, float, bool)

class D:
    def __init__(self, data):
        self.data = data


___ = D("")


class DesignConfig:

    def __init__(self, environ: Union[dict,os._Environ[str]] = os.environ):
        self._environ = environ

        for key in dir(self):
            value = getattr(self, key)

            if not key.startswith('_') and type(value) == D:

                type_value = type(value.data)

                assert type_value in [str, bool, int, float], \
                    f"D-function only handles atomic values, not {type_value}"

                if key not in self._environ:
                    value = value.data
                else:
                    value = self._environ[key]

                    if type_value is bool:
                        if type(value) == str:
                            if value.lower() in ['false','no','0']:
                                value = False
                        value = bool(value)
                    elif type_value is int:
                        try:
                            value = int(value)
                        except ValueError:
                            value = 0
                    elif type_value is float:
                        try:
                            value = float(value)
                        except ValueError:
                            value = 0.0
                
                setattr(self, key, value)

        for key in dir(self):
            value = getattr(self, key)

            if not key.startswith('_') and type(value) == str:
                setattr(self, key, self._get_format_str(value)) 


    def __call__(self, key: str, default: T) -> T:
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return default

    def __getitem__(self, template:str) -> str:
        if type(template) != str:
            return template

        reg = re.compile(r'{([^{}]*)}')
        if not reg.search(template):
            return self._get_str(template)

        template = self._get_format_str(template)
        return template


    def __str__(self):
        return '\n'.join([f'{attr}\t->\t{self._get_str(attr)}' for attr in dir(self) if not attr.startswith('_')])


    def _get_str(self, key: str, default: str = '') -> str:
        if hasattr(self, key):
            value = getattr(self, key)
            if type(value) == str:
                return self._get_format_str(value)
            else:
                return str(value)
        elif default != '':
            return default
        else:
            return key


    def _get_format_str(self, template: str, path=()) -> str:
        if len(path) != len(set(path)):
            return template
        reg = re.compile(r'{([^{}]*)}')
        if reg.search(template):
            return template.format(**{key: self._get_format_str(self._get_str(key), path+(key,)) for key in reg.findall(template)})
        else:
            return template

