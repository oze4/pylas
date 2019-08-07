class PylasDict(dict):
    """
    dot.notation access to dictionary attributes.

    Instead of having to access attributes in a dict like `obj["attribute"]`, this
    class allows you to access attributes like `obj.attribute`.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__