from pylas.pylasClasses import PylasAsListOrDict, PylasDict
from pylas import pylasIO
from pylas import pylasText
from pylas import pylasCore


"""
TODO: Still in progress - finish building out this file
"""


def ConvertLasToJson(lasFilePath: str) -> dict:
    """
    :param str lasFilePath: Path to .las file
    """
    try:
        fullLasFileString = pylasIO.readLasFile(lasFilePath)
        sections = pylasText.splitLasSections(fullLasFileString)

        output = {
            "WellInformationDict": pylasCore.convertWellInfoToDict(sections.WellInformation),
            "WellInformationList": pylasCore.convertWellInfoToList(sections.WellInformation)
        }

        return PylasDict(output)

    except Exception as e:
        base_error_message = "\n\nSomething went wrong converting las to json!\n\n"
        print(e, base_error_message, repr(e))
