from .pylasClasses import PylasSectionType, PylasAsListOrDict, PylasDict
from pylas import pylasRegex
from pylas import pylasText


def unwrapCurveData(wrappedCurveDataString: str) -> str:
    """
    1. A wrapped curve data section can only be max 80 characters
    2. Each header row of the curve data section starst with a # sign
    3. Need to count the number of lines with a # sign so I can parse each line of the overall curve data in a loop,
       and then create sub loops of X length (where X is the number of # signs), so I can concatenate those X number
       of lines, therefore creating a 'normal' unwrapped line
    """
    try:
        if not wrappedCurveDataString.lower().startswith(PylasSectionType.curve_data.value):
            err = "\n\n[convertCurveDataToListOfDicts]::Incorrect Curve Data section string supplied!\n\n"
            raise Exception(err)
        
        header_line_count = 0
        curves_string_list = wrappedCurveDataString.split("\n")

        for line in curves_string_list:
            if line.lower().startswith(PylasSectionType.curve_data.value):  # This is for the '~A  Depth' header line, which is usually on its own line
                header_line_count = header_line_count + 1
                print(line)
            elif line.startswith("#"):    # This is for all other header lines
                header_line_count = header_line_count + 1
                print(line)
            else:
                break

        return header_line_count
    except Exception as e:
        return e


def convertCurveDataToListOfDicts(curveDataSectionString: str) -> list:
    """
    :param str curveDataSectionString: curve data section as a string

    Converts las curve data section/block (the table at the bottom of a las file) into a list of dicts, 
    each curve will be its own dict in the list.
    """    
    try:         
        if not curveDataSectionString.lower().startswith(PylasSectionType.curve_data.value):
            err = "\n\n[convertCurveDataToListOfDicts]::Incorrect Curve Data section string supplied!\n\n"
            raise Exception(err)
        else:
            curves = []
            curvesStringList = curveDataSectionString.split("\n")
            curvesHeaderList = pylasRegex.trimMultipleSpaces(curvesStringList[0]).split(" ")

            for name in curvesHeaderList:
                curveObj = {}
                if name.strip().lower() != "a":
                    curveObj["name"] = name
                    curveObj["data"] = []
                    curves.append(PylasDict(curveObj))

            curvesStringBody = curvesStringList
            curvesStringBody.pop(0)  # Remove first item in list (this removes the header row so we can parse curve values)

            for i in range(len(curvesStringBody)):
                bodyLineString = pylasRegex.trimMultipleSpaces(curvesStringBody[i])
                bodyLineList = bodyLineString.split(" ")
                for index, val in enumerate(bodyLineList):
                    curves[index].data.append(val)

            return curves
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        base_err_message = f"[convertCurveDataToListOfDicts]::[ERROR] Something went wrong converting curve data to list of dicts! At line {exc_tb.tb_lineno}"
        print(base_err_message, repr(e))


def convertWrapLineToObject(rawWrapLine: str) -> dict:
    """
    :param str rawWrapLine: The raw string (from the Version Information block) which contains the Wrap info

    Converts the Wrap line from the Version Information section/block into an object.
    """
    trimmed = rawWrapLine.strip()
    if trimmed.startswith("WRAP."):
        cleanedString = pylasRegex.trimMultipleSpaces(trimmed)
        output =  pylasText.lasLineToDict(cleanedString)
        return PylasDict(output)
    else:
        err = "[convertWrapLineToObject]::Incorrect raw Wrap line supplied!"
        raise Exception(err)


def convertVersionLineToObject(rawVersionLine: str) -> dict:
    """
    :param str rawVersionLine: The raw string (from the Version Information block) which contains the las file Version info

    Converts the actual las file Version line from the Version Information section/block into an object.
    """
    trimmed = rawVersionLine.strip()
    if trimmed.startswith("VERS."):
        cleanedString = pylasRegex.trimMultipleSpaces(trimmed)
        output = pylasText.lasLineToDict(cleanedString)
        return PylasDict(output)
    else:
        err = "[convertVersionLineToObject]::Incorrect raw Version line supplied!"
        raise Exception(err)


def convertCurveInfoToDict(rawCurveInfoSectionString: str) -> dict:
    """
    :param str rawCurveInfoSectionString: The raw string for the Curve Information section/block

    Converts a single line from raw Curve Information section/block to dict
    """
    section = PylasSectionType.curve_information
    out_as = PylasAsListOrDict.as_dict
    output = __convertSectionStringToObject(rawCurveInfoSectionString, section, out_as)
    return PylasDict(output)


def convertCurveInfoToList(rawCurveInfoSectionString: str) -> list:
    """
    :param str rawCurveInfoSectionString: The raw string for the Curve Information section/block

    Converts a single line from raw Curve Information section/block to a list    
    """
    section = PylasSectionType.curve_information
    out_as = PylasAsListOrDict.as_list
    output = __convertSectionStringToObject(rawCurveInfoSectionString, section, out_as)
    return PylasDict(output)


def convertWellInfoToList(rawWellInfoSectionString: str) -> dict:
    """
    :param str rawWellInfoSectionString: The raw string for the Well Information section/block

    Converts a single line from raw Well Information section/block to a list
    """
    section = PylasSectionType.well_information_bock
    out_as = PylasAsListOrDict.as_list  # output as list
    output = __convertSectionStringToObject(rawWellInfoSectionString, section, out_as)
    return PylasDict(output)


def convertWellInfoToDict(rawWellInfoSectionString: str) -> dict:
    """
    :param str rawWellInfoSectionString: The raw string for the Well Information section/block

    Converts a single line from raw Well Information section/block to a dict
    """
    section = PylasSectionType.well_information_bock
    out_as = PylasAsListOrDict.as_dict  # output as dict
    output = __convertSectionStringToObject(rawWellInfoSectionString, section, out_as)
    return PylasDict(output)


def convertParameterInfoToDict(rawParameterInfoSectionString: str) -> dict:
    """
    :param str rawParameterInfoSectionString: The raw string for the Parameter Information Block

    Converts a single line from raw Parameter Information section/block to a dict    
    """
    section = PylasSectionType.parameter_information_block
    out_as = PylasAsListOrDict.as_dict
    output = __convertSectionStringToObject(rawParameterInfoSectionString, section, out_as)
    return PylasDict(output)


def __convertSectionStringToObject(rawSectionString: str, startsWith: PylasSectionType, outputAs: PylasAsListOrDict) -> dict:  # OR -> list
    """
    :param str rawSectionString: The raw las section as a string
    :param PylasSectionType (Enum) startsWith: The LOWER CASE section header
        - for example: 
            - 'well information block' for well info
            - 'curve information' for curve info
            - 'a  ' for curve DATA - 2 spaces after 'a' are required!
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
            return PylasDict(__sectionStringToDict(rawSectionString))
        if outputAs.value == "list":
            return PylasDict(__sectionStringToList(rawSectionString))
    else:
        exception = f"[__convertSectionStringToObject[{startsWith.value}]]::Unable to convert section to object!"
        raise Exception(exception)


def __sectionStringToDict(rawSectionString: str) -> dict:
    """
    Converts raw section string to DICT. The MNEMONIC from each line is used as the key on the output object.
    """
    output = {}
    for line in rawSectionString.split("\n"):
        out = pylasText.lasLineToDict(line)
        if len(list(out.keys())) > 0:
            output[out.Mnemonic] = out
    return PylasDict(output)


def __sectionStringToList(rawSectionString: str) -> list:
    """
    Converts raw section string to LIST.
    """
    output = []
    for line in rawSectionString.split("\n"):
        out = pylasText.lasLineToDict(line)
        if len(list(out.keys())) > 0:
            output.append(out)
    # Since it is a list, we don't have to apply PylasDict            
    return output  