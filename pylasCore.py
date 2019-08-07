import pylasRegex
import pylasText



def convertWrapLineStringToObject(rawWrapLine:str) -> dict:
    trimmed = rawWrapLine.strip()
    if trimmed.startswith("WRAP."):
        cleanedString = pylasRegex.replaceMultipleSpacesWithSingleSpace(trimmed)
        return pylasText.createObjectFromLasString(cleanedString)
    else:
        raise Exception("[convertWrapLineStringToObject]::Incorrect raw Wrap line supplied!")



def convertVersionLineStringToObject(rawVersionLine:str) -> dict:
    trimmed = rawWrapLine.strip()
    if trimmed.startswith("VERS."):
        cleanedString = pylasRegex.replaceMultipleSpacesWithSingleSpace(trimmed)
        return pylasText.createObjectFromLasString(cleanedString)
    else:
        raise Exception("[convertVersionLineStringToObject]::Incorrect raw Version line supplied!")



def convertCurveInfoSectionStringToObject(rawCurveInfoSectionString:str) -> dict:
    if rawCurveInfoSectionString.lower().startswith("curve information"):
        curves = []
        for curveInfoSection in rawCurveInfoSectionString.split("\n"):
            curveObj = pylasText.createObjectFromLasString(curveInfoSection)
            if len(list(curveObj.keys())) > 0:
                curves.append(curveObj)

        return curves
    
    else:
        raise Exception("[covertCurveInfoSectionStringToObject]::Incorrect Curve Information section string supplied!")
