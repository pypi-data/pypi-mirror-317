import os

from ROTools.Helpers.Attr import setattr_ex, getattr_ex
from ROTools.Helpers.DictObj import DictObj

class Config(DictObj):
    def __init__(self, **kwargs):
        super().__init__()
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def add_env_data(self, prefix):
        extra_config = [(key[len(prefix):].lower(), value) for key, value in os.environ.items() if key.startswith(prefix)]

        for key, value in extra_config:
            _old_value = getattr_ex(self, key)
            if _old_value is not None and isinstance(_old_value, bool):
                setattr_ex(self, key, value in ["true", "True", "TRUE", "1", ])
                continue

            if _old_value is not None and isinstance(_old_value, int):
                setattr_ex(self, key, int(value))
                continue

            if _old_value is not None and isinstance(_old_value, float):
                setattr_ex(self, key, float(value))
                continue

            setattr_ex(self, key, value)

    def dump_config(self):
        print()
        print("========")
        self.dump()
        print("========")
        print()
