from pylasClasses import PylasDict
import pylasRegex


def createObjectFromLasString(singleLineString:str) -> dict:
    """
    TLDR;Separates each piece of a SINGLE las file line into an object/dict that can be
    appended to a larger object.  

    This method takes a single line from a las file heading and puts 
    each defined piece of data, as outlined in the CWLS spec, as its own 'property'
    on an object/dict. That object/dict is what this method returns, which will
    be appended to a larger object/dict.
    """
    try:
        mnem = pylasRegex.getMnemonicKeyFromString(singleLineString)
        val = pylasRegex.getMnemonicValueFromString(singleLineString)
        units = pylasRegex.getUnitsFromString(singleLineString)
        desc = pylasRegex.getDescriptionFromString(singleLineString)

        output = {}
        if mnem:
            output["Mnemonic"] = pylasRegex.replaceMultipleSpacesWithSingleSpace(mnem)
        if val:
            output["Value"] = pylasRegex.replaceMultipleSpacesWithSingleSpace(val)
        if units:
            output["Unit"] = pylasRegex.replaceMultipleSpacesWithSingleSpace(units)
        if desc:
            output["Description"] = pylasRegex.replaceMultipleSpacesWithSingleSpace(desc)

        return PylasDict(output)

    except Exception as e:
        base_error_message = "\n\n[createObjectFromLasString]::Something went wrong converting singleLineString to {Mnem,Val,Units,Desc} Object\n\n"
        print(e, base_error_message, repr(e))


def splitLasSectionsIntoBlockStrings(lasFileString:str) -> dict:
    """
    Separates each section of the entire las file into raw strings according to the
    type of data the section holds.
    """
    try:
        split = []
        for section in lasFileString.split("~"):
            if section != "":
                split.append(section)

        sectionStrings = {}
        for i in range(len(split)):
            line = split[i]
            lowercase_line = line.lower()
            if "version" in lowercase_line:
                sectionStrings["VersionInformation"] = line
            elif "well information" in lowercase_line:
                sectionStrings["WellInformation"] = line
            elif "curve information" in lowercase_line:
                sectionStrings["CurveInformation"] = line
            elif "parameter" in lowercase_line:
                sectionStrings["ParameterInformation"] = line
            elif "other" in lowercase_line:
                sectionStrings["Other"] = line
            elif "a  depth" in lowercase_line:
                sectionStrings["Curves"] = line

        return PylasDict(sectionStrings)

    except Exception as e:
        raise e


def getVersionLine(versionBlockString:str) -> str:
    """ 
    TODO:Should be renamed to 'getLasFileVersionLine' or something like it..

    The raw version information is 3 lines, which contain the (1) las file version
    as well as (2) whether or not the las file is wrapped. This method gets the Version Info
    """
    if "version information" in versionBlockString.split("\n")[0].lower():
        return versionBlockString.split("\n")[1]
    else:
        raise Exception("[getVersionLine]::Incorrect version string supplied!")


def getWrapLine(versionBlockString:str) -> str:
    """ 
    The raw version information is 3 lines, which contain the (1) las file version
    as well as (2) whether or not the las file is wrapped. This method gets the Wrap Info
    """
    if "version information" in versionBlockString.split("\n")[0].lower():
        return versionBlockString.split("\n")[2]
    else:
        raise Exception("[getWrapLine]::Incorrect version string supplied!")
