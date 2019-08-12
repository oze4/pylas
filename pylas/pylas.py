from .pylasClasses import PylasAsListOrDict, PylasDict
from pylas import pylasIO
from pylas import pylasText
from pylas import pylasCore


def ConvertLasToJson(lasFilePath: str) -> dict:
    """
    :param str lasFilePath: Path to .las file

    Converts .las file into a dict/json format. Dynamically and automatically determines 
    if a .las files is wrapped or not, and will parse the file accordingly.
    """
    try:
        fullLasFileString = pylasIO.readLasFile(lasFilePath)
        sections = pylasText.splitLasSections(fullLasFileString)

        versionString = pylasText.getVersionLine(sections.VersionInformation)
        versionInfoObject = pylasCore.convertVersionLineToObject(versionString)
        wrapString = pylasText.getWrapLine(sections.VersionInformation)
        wrapInfoObject = pylasCore.convertWrapLineToObject(wrapString)

        staged_output = {
            "VersionInformation": {
                "Version": versionInfoObject,
                "Wrap": wrapInfoObject,
            },
            "WellInformation": pylasCore.convertWellInfoToDict(sections.WellInformation),
            "CurveInformation": pylasCore.convertCurveInfoToDict(sections.CurveInformation),            
        }

        if "ParameterInformation" in sections.keys():
            param_info = pylasCore.convertParameterInfoToDict(sections.ParameterInformation)
            if len(param_info.keys()) > 0:
                staged_output["ParameterInformation"] = param_info

        if "Other" in sections.keys():
            other_info = pylasCore.convertOtherSection(sections.Other)
            if other_info != "":
                staged_output["Other"] = other_info        

        # If .las file is wrapped
        if wrapInfoObject.Value == "NO":
            staged_output["Curves"] = pylasCore.convertCurveDataToListOfDicts(sections.Curves) 
        # If .las file is unwrapped (not wrapped)
        elif wrapInfoObject.Value == "YES":
            unwrapped_curves_data = pylasCore.unwrapCurveData(sections.Curves)
            curvesDataObject = pylasCore.convertCurveDataToListOfDicts(unwrapped_curves_data)
            staged_output["Curves"] = curvesDataObject                   

        # START: RETURN DATA HERE
        return PylasDict(staged_output)
        # END: RETURN DATA HERE

    except Exception as e:
        base_error_message = f"\n\nSomething went wrong converting las to json!\n\n[FilePath]:: '{lasFilePath}'"
        print(e, base_error_message, repr(e))
