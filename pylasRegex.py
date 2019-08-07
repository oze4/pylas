import re


test_string_for_regex = "UWI.           37-129-28930-00-01: UNIQUE WELL ID"


def getMatch(regexResults:list) -> str:
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


def replaceMultipleSpacesWithSingleSpace(string:str) -> str:
    """
    Replaces multiple spaces swith single space
    """
    return ' '.join(string.split()).strip()


def getMnemonicKeyFromString(string:str) -> list:
    """
    Grabs the mnemonic from a las file line. In the following example, "UWI" is returned:
    "UWI.           37-129-28930-00-01: UNIQUE WELL ID"
    """
    res = re.findall(r'.+?(?=\.)', string)
    return getMatch(res)
