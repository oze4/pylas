import re


def replaceMultipleSpacesWithSingleSpace(string):
    return ' '.join(string.split()).strip()


def getMnemonicKeyFromString(string):
    return re.match(r'/.+?(?=\.)/g', string)
