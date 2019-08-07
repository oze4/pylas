from pylas.pylasClasses import PylasSectionType, PylasAsListOrDict, PylasDict
from pylas import pylasRegex
from pylas import pylasText


def convertWrapLineToObject(rawWrapLine: str) -> dict:
    """
    :param str rawWrapLine: The raw string (from the Version Information block) which contains the Wrap info

    Converts the Wrap line from the Version Information section/block into an object.
    """
    trimmed = rawWrapLine.strip()
    if trimmed.startswith("WRAP."):
        cleanedString = pylasRegex.trimMultipleSpaces(trimmed)
        return pylasText.lasLineToDict(cleanedString)
    else:
        err = "[convertWrapLineToObject]::Incorrect raw Wrap line supplied!"
        raise Exception(err)


def convertVersionLineToObject(rawVersionLine: str) -> dict:
    """
    :param str rawVersionLine: The raw string (from the Version Information block) which contains the las file Version info

    Converts the actual las file Version line from the Version Information section/block into an object.
    """
    trimmed = rawWrapLine.strip()
    if trimmed.startswith("VERS."):
        cleanedString = pylasRegex.trimMultipleSpaces(trimmed)
        return pylasText.lasLineToDict(cleanedString)
    else:
        err = "[convertVersionLineToObject]::Incorrect raw Version line supplied!"
        raise Exception(err)


def convertCurveInfoToObject(rawCurveInfoSectionString: str) -> dict:
    """
    :param str rawCurveInfoSectionString: The raw string for the Curve Information section/block

    Converts raw Curve Information section/block to an object (dict)
    """
    return __convertSectionStringToObject(
        rawCurveInfoSectionString,
        PylasSectionType.curve_information
    )


def convertWellInfoToList(rawWellInfoSectionString: str) -> dict:
    """
    :param str rawWellInfoSectionString: The raw string for the Well Information section/block

    Converts raw Well Information section/block to a list
    """
    section = PylasSectionType.well_information_bock
    out_as = PylasAsListOrDict.as_list  # output as list
    return __convertSectionStringToObject(rawWellInfoSectionString, section, out_as)


def convertWellInfoToDict(rawWellInfoSectionString: str) -> dict:
    """
    :param str rawWellInfoSectionString: The raw string for the Well Information section/block

    Converts raw Well Information section/block to a dict
    """
    section = PylasSectionType.well_information_bock
    out_as = PylasAsListOrDict.as_dict  # output as dict
    return __convertSectionStringToObject(rawWellInfoSectionString, section, out_as)


def __convertSectionStringToObject(rawSectionString: str, startsWith: PylasSectionType, outputAs: PylasAsListOrDict) -> dict:  # OR -> list
    """
    :param str rawSectionString: The raw las section as a string
    :param PylasSectionType (Enum) startsWith: The LOWER CASE section
    :param PylasAsListOrDict (Enum) outputAs: The output formatting of the newly created object
    :returns [dict|list]: Depending upon which parameter you use

    Converts any raw las section string to an object. This method essentially loops through each line in a las section
    and converts each line to an object, which gets added to a larger object. The MNEMONIC from each line is used as the key
    on the larger object.

    We do this using `pylasText.lasLineToDict(theSectionString)` 
        (which is inside both methods: `__sectionStringToDict(...)` & `__sectionStringToList(...)`)
    """
    if type(startsWith).__name__ != "PylasSectionType":
        err = "[__convertSectionStringToObject]::PARAMETER ERROR: Parameter 'startsWith' must be an enum from 'PylasSectionType'!"
        raise Exception(err)
    if type(outputAs).__name__ != "PylasAsListOrDict":
        errr = "[__convertSectionStringToObject]::PARAMETER ERROR: Parameter 'outputAs' must be an enum from 'PylasAsListOrDict'!"
        raise Exception(errr)

    if rawSectionString.lower().startswith(startsWith.value):
        if outputAs.value == "dict":
            return __sectionStringToDict(rawSectionString)
        if outputAs.value == "list":
            return __sectionStringToList(rawSectionString)
    else:
        exception = f"[__convertSectionStringToObject[{startsWith.value}]]::Unable to convert section to object!"
        raise Exception(exception)


def __sectionStringToDict(rawSectionString: str) -> dict:
    """
    Converts raw section string to DICT. The MNEMONIC from each line is used as the key on the output object.
    """
    output = {}
    for section in rawSectionString.split("\n"):
        out = pylasText.lasLineToDict(section)
        if len(list(out.keys())) > 0:
            output[out.Mnemonic] = out
    return PylasDict(output)


def __sectionStringToList(rawSectionString: str) -> list:
    """
    Converts raw section string to LIST.
    """
    output = []
    for section in rawSectionString.split("\n"):
        out = pylasText.lasLineToDict(section)
        if len(list(out.keys())) > 0:
            output.append(out)
    return output
