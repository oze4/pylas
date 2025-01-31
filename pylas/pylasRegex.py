import re


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


def getMnemonicKeyFromString(string: str) -> str:
    """
    Grabs the mnemonic from a las file line. In the following example, "UWI" is returned:
    "UWI.           37-129-28930-00-01: UNIQUE WELL ID"
    """
    res = re.findall(r'.+?(?=\.)', string)
    return getMatch(res)


def getMnemonicValueFromString(string: str) -> str:
    """ 
    Other possible solutions:
      >>    [original solution] (?<=. ).*?(?=:)
      >>    (?<=.) .*?:
      >>    (?<=.) .*(?=\s*:)
    Grabs the value of the mnemonic from a las file line. In the following example, "Lat: 00.000000--Long: -11.111111----" is returned:
    "LOC.           Lat: 00.000000--Long: -11.111111----: LOCATION"
    """
    res = re.findall(r"(?<=.) .*(?=\s*:)", string)
    return getMatch(res)


def getDescriptionFromString(string: str) -> str:
    """
    Grabs the description from a las file line. In the following example, "UNIQUE WELL ID" is returned:
    "UWI.           37-129-28930-00-01: UNIQUE WELL ID"
    """
    res = re.findall(r'(?<=: ).*', string)
    return getMatch(res)


def getUnitsFromString(string: str) -> str:
    """
    Grabs the units (unit of measurement) from a las file line. In the following example, "FT" is returned:
    "STRT.FT              8295.5000: START DEPTH"
    """
    res = re.findall(r'(?<=\.).*?(?= )', string)
    return getMatch(res)
