import pylasIO
import pylasText



def ConvertLasToJson(lasFilePath):
    try:
        fullLasFileString = pylasIO.readLasFile(lasFilePath)
        lasSectionBlockStrings = pylasText.splitLasSectionsIntoBlockStrings(fullLasFileString)
        return lasSectionBlockStrings

    except Exception as e:
        base_error_message = "\n\nSomething went wrong converting las to json!\n\n"
        print(e, base_error_message, repr(e))



lasJson = ConvertLasToJson("./las_files/las_with_lat_lon.las")
print(lasJson.WellInformation)
