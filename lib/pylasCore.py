from pylasClasses import PylasSectionType
import pylasRegex
import pylasText


def convertWrapLineToObject(rawWrapLine: str) -> dict:
    """ ~~~ TODO: could most likely create one method to dynamically handle this method as well as `convertVersionLineToObject`,
                  similar to how I am using `__convertSectionStringToObject` ~~~
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
    return __convertSectionStringToList(
        rawWellInfoSectionString,
        PylasSectionType.well_information_bock
    )


def convertWellInfoToDict(rawWellInfoSectionString: str) -> dict:
    """
    :param str rawWellInfoSectionString: The raw string for the Well Information section/block

    Converts raw Well Information section/block to a dict
    """
    return __convertSectionStringToDict(
        rawWellInfoSectionString,
        PylasSectionType.well_information_bock
    )    


def __convertSectionStringToList(rawSectionString: str, startsWith: PylasSectionType) -> list:
    """
    :param str rawSectionString: The raw las section as a string
    :param str startsWith: The LOWER CASE section

    Converts any raw las section string to an object. This method essentially loops through each line in a las section
    and converts each line to an object, which gets appended to a list.

    We do this using `pylasText.lasLineToDict(theSectionString)`
    """
    if type(startsWith).__name__ != "PylasSectionType":
        raise Exception(
            "[convertSectionStringToObject]::PARAMETER ERROR: Parameter 'startsWith' must be an enum from 'PylasSectionType'!")
    else:
        if rawSectionString.lower().startswith(startsWith.value):
            output = []
            for section in rawSectionString.split("\n"):
                out = pylasText.lasLineToDict(section)
                if len(list(out.keys())) > 0:
                    output.append(out)
            return output
        else:
            exception = f"[convertSectionStringToObject[{startsWith.value}]]::Unable to convert section to object!"
            raise Exception(exception)


def __convertSectionStringToDict(rawSectionString: str, startsWith: PylasSectionType) -> dict:
    """
    :param str rawSectionString: The raw las section as a string
    :param str startsWith: The LOWER CASE section

    Converts any raw las section string to an object. This method essentially loops through each line in a las section
    and converts each line to an object, which gets added to a larger object. The MNEMONIC from each line is used as the key
    on the larger object.

    We do this using `pylasText.lasLineToDict(theSectionString)`
    """
    if type(startsWith).__name__ != "PylasSectionType":
        raise Exception(
            "[convertSectionStringToObject]::PARAMETER ERROR: Parameter 'startsWith' must be an enum from 'PylasSectionType'!")
    else:
        if rawSectionString.lower().startswith(startsWith.value):
            output = {}
            for section in rawSectionString.split("\n"):
                out = pylasText.lasLineToDict(section)
                if len(list(out.keys())) > 0:
                    output[out.Mnemonic] = out
            return output
        else:
            exception = f"[convertSectionStringToObject[{startsWith.value}]]::Unable to convert section to object!"
            raise Exception(exception)            
