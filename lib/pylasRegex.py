import re


test_string_for_regex1 = "UWI.           37-129-28930-00-01: UNIQUE WELL ID"
test_string_for_regex2 = "LOC.           Lat 40.426716--Long -79.54976: LOCATION"
test_string_for_regex3 = "STRT.FT              8295.5000: START DEPTH"
test_string_for_regex4 = "LOC.           Lat: 40.487717--Long: -80.733858----: LOCATION"


def getMatch(regexResults: list) -> str:
    """
    Gets the first result in array of re.findall(...) matches
    """
    try:
        output = False
        if len(regexResults) > 0:
            output = regexResults[0]
        return output
    except:
        return False


def trimMultipleSpaces(string: str) -> str:
    """
    Replaces multiple spaces swith single space
    """
    return ' '.join(string.split()).strip()


def getMnemonicKeyFromString(string: str) -> list:
    """
    Grabs the mnemonic from a las file line. In the following example, "UWI" is returned:
    "UWI.           37-129-28930-00-01: UNIQUE WELL ID"
    """
    res = re.findall(r'.+?(?=\.)', string)
    return getMatch(res)


def getMnemonicValueFromString(string: str) -> list:
    """ 
    Other possible solutions:
      >>    [original solution] (?<=. ).*?(?=:)
      >>    (?<=.) .*?:
      >>    (?<=.) .*(?=\s*:)
    Grabs the value of the mnemonic from a las file line. In the following example, "Lat: 40.487717--Long: -80.733858----" is returned:
    "LOC.           Lat: 40.487717--Long: -80.733858----: LOCATION"
    """
    res = re.findall(r"(?<=.) .*(?=\s*:)", string)
    return getMatch(res)


def getDescriptionFromString(string: str) -> list:
    """
    Grabs the description from a las file line. In the following example, "UNIQUE WELL ID" is returned:
    "UWI.           37-129-28930-00-01: UNIQUE WELL ID"
    """
    res = re.findall(r'(?<=: ).*', string)
    return getMatch(res)


def getUnitsFromString(string: str) -> list:
    """
    Grabs the units (unit of measurement) from a las file line. In the following example, "FT" is returned:
    "STRT.FT              8295.5000: START DEPTH"
    """
    res = re.findall(r'(?<=\.).*?(?= )', string)
    return getMatch(res)
