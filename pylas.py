import pylasIO
import pylasText


fullLasFileString = pylasIO.readLasFile("./las_files/las_with_lat_lon.las")

lasSectionBlockStrings = pylasText.splitLasSectionsIntoBlockStrings(fullLasFileString)
print(lasSectionBlockStrings["WellInformation"])
