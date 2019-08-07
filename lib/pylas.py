import pylasIO
import pylasText
import pylasCore


"""
TODO: Still in progress - finish building out this file
"""

def ConvertLasToJson(lasFilePath):
    try:
        fullLasFileString = pylasIO.readLasFile(lasFilePath)
        lasSectionBlockStrings = pylasText.splitLasSections(fullLasFileString)
        return lasSectionBlockStrings

    except Exception as e:
        base_error_message = "\n\nSomething went wrong converting las to json!\n\n"
        print(e, base_error_message, repr(e))


lasJson = ConvertLasToJson("./las_files/las_with_lat_lon.las")
well_info_list = pylasCore.convertWellInfoToList(lasJson.WellInformation)
well_info_dict = pylasCore.convertWellInfoToDict(lasJson.WellInformation)

print(well_info_list)
print("")
print(well_info_dict)
