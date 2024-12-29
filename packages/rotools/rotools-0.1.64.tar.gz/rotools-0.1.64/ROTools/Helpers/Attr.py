def getattr_ex(_obj, name):
    if isinstance(name, str):
        name = name.split(".")

    if isinstance(name, list):
        for item in name:
            if _obj is None:
                return None
            _obj = getattr(_obj, item, None)
        return _obj

    raise Exception("Param error")


def setattr_ex(_obj, name, value, parent_class=object):
    if isinstance(name, str):
        name = name.split(".")

    if isinstance(name, list):
        for item in name[:-1]:
            _next = getattr(_obj, item, None)
            if _next is None:
                _next = parent_class()
                setattr(_obj, item, _next)
            _obj = _next
        setattr(_obj, name[-1], value)
        return

    raise Exception("Param error")


def hasattr_ex(_obj, name):
    if isinstance(name, str):
        name = name.split(".")

    if isinstance(name, list):
        for i, item in enumerate(name):
            is_last = i == len(name) - 1
            if hasattr(_obj, item) is False:
                return False
            _obj = getattr(_obj, item, None)
            if _obj is None and not is_last:
                return False
        return True

    raise Exception("Param error")
