import copy

from ROTools.Helpers.Attr import setattr_ex, hasattr_ex
from ROTools.Helpers.DumpBase import DumpBase


def _gen_fields_list(obj, current_path=None):
    if not isinstance(obj, DictObj):
        return [(current_path, obj)]
    result = []
    for key, value in obj.items():
        next_path = ".".join([a for a in (current_path, key) if a is not None])

        if isinstance(value, DictObj):
            result.extend(_gen_fields_list(value, current_path=next_path))
        else:
            result.append((next_path, value))
    return result


class DictObj(DumpBase):
    def __init__(self, d=None):
        if d is None:
            return
        if isinstance(d, DictObj):
            for k, v in d.__dict__.items():
                self.__dict__[k] = copy.deepcopy(v)
            return

        if isinstance(d, dict):
            self._build_dict(d)
            return

        raise Exception("Flow")

    def _build_dict(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DictObj(x) if isinstance(x, dict) else x for x in b])
                continue
            setattr(self, a, DictObj(b) if isinstance(b, dict) else b)

    def get(self, name, default=None):
        return getattr(self, name, default)

    def set(self, path, value):
        return setattr_ex(self, path, value, parent_class=DictObj)

    def to_dict(self):
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, DictObj):
                v = v.to_dict()
            result[k] = v
        return result

    def set_values(self, values, only_if_exists=True):
        for path, nev_value in values:
            if only_if_exists and not hasattr_ex(self, path):
                continue
            self.set(path, nev_value)

    def fields_list(self):
        return _gen_fields_list(self)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def clone(self):
        import copy
        return copy.deepcopy(self)
