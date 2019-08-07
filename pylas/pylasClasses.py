from enum import Enum


class PylasDict(dict):
    """
    dot.notation access to dictionary attributes.

    Instead of having to access attributes in a dict like `obj["attribute"]`, this
    class allows you to access attributes like `obj.attribute`.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class PylasSectionType(Enum):
    """
    This class is used to validate certain parameters on other methods. Pseudo 'type validation'.
    """
    well_information_bock = "well information block"
    curve_information = "curve information"
    curve_data = "a  "


class PylasAsListOrDict(Enum):
    """
    This class is used for validating parameter types when converting a las section/block to object.
    Used in pylasCore -> __convertSectionStringToListOrDict(...)
    """
    as_list = "list"
    as_dict = "dict"
