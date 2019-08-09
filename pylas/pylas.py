from .pylasClasses import PylasAsListOrDict, PylasDict
from pylas import pylasIO
from pylas import pylasText
from pylas import pylasCore


def ConvertLasToJson(lasFilePath: str) -> dict:
    """
    :param str lasFilePath: Path to .las file
    """
    try:
        fullLasFileString = pylasIO.readLasFile(lasFilePath)
        sections = pylasText.splitLasSections(fullLasFileString)

        versionString = pylasText.getVersionLine(sections.VersionInformation)
        versionInfoObject = pylasCore.convertVersionLineToObject(versionString)
        wrapString = pylasText.getWrapLine(sections.VersionInformation)
        wrapInfoObject = pylasCore.convertWrapLineToObject(wrapString)

        # ONLY PROCESS LAS FILE IF IT IS NOT WRAPPED!!
        # We currently do not support wrapped .las files
        if wrapInfoObject.Value == "NO":
            wellInfoObject = pylasCore.convertWellInfoToDict(sections.WellInformation)
            curveInfoObject = pylasCore.convertCurveInfoToDict(sections.CurveInformation)
            curvesDataObject = pylasCore.convertCurveDataToListOfDicts(sections.Curves)

            staged_output = {
                "VersionInformation": {
                    "Version": versionInfoObject,
                    "Wrap": wrapInfoObject
                },
                "WellInformation": wellInfoObject,
                "CurveInformation": curveInfoObject,
                "Curves": curvesDataObject
            }

            if "ParameterInformation" in sections.keys():
                staged_output["ParameterInformation"] = pylasCore.convertParameterInfoToDict(sections.ParameterInformation)

            output = PylasDict(staged_output)
            return output

        else:
            print(f"[SKIPPING]::Wrapped .las file found! '{lasFilePath}'")

    except Exception as e:
        base_error_message = f"\n\nSomething went wrong converting las to json!\n\n[FilePath]:: '{lasFilePath}'"
        print(e, base_error_message, repr(e))


def ConvertLasToJsonWRAPPED(lasFilePath: str) -> dict:
    """
    :param str lasFilePath: Path to .las file
    """
    try:
        fullLasFileString = pylasIO.readLasFile(lasFilePath)
        sections = pylasText.splitLasSections(fullLasFileString)

        versionString = pylasText.getVersionLine(sections.VersionInformation)
        versionInfoObject = pylasCore.convertVersionLineToObject(versionString)
        wrapString = pylasText.getWrapLine(sections.VersionInformation)
        wrapInfoObject = pylasCore.convertWrapLineToObject(wrapString)

        # ONLY PROCESSES WRAPPED LAS FILES!
        # Using this for testing...
        if wrapInfoObject.Value == "YES":
            wellInfoObject = pylasCore.convertWellInfoToDict(sections.WellInformation)
            curveInfoObject = pylasCore.convertCurveInfoToDict(sections.CurveInformation)
            unwrapped_curves_data = pylasCore.unwrapCurveData(sections.Curves)
            #curvesDataObject = pylasCore.convertCurveDataToListOfDicts(unwrapped_curves_data)

            staged_output = {
                "VersionInformation": {
                    "Version": versionInfoObject,
                    "Wrap": wrapInfoObject
                },
                "WellInformation": wellInfoObject,
                "CurveInformation": curveInfoObject,
                "Curves": unwrapped_curves_data#curvesDataObject
            }

            if "ParameterInformation" in sections.keys():
                staged_output["ParameterInformation"] = pylasCore.convertParameterInfoToDict(sections.ParameterInformation)

            output = PylasDict(staged_output)
            return output

        else:
            print(f"[SKIPPING]::UNwrapped .las file found! '{lasFilePath}'")

    except Exception as e:
        base_error_message = f"\n\nSomething went wrong converting las to json!\n\n[FilePath]:: '{lasFilePath}'"
        print(e, base_error_message, repr(e))
 