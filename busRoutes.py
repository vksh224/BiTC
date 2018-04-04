from map_plot_Dgr import *
from computeHarvesine import *
from pathlib import Path

def printTimes(times):
    if len(times) == 0:
        print("none")
    else:
        for i in range(len(times)):
            print(str(times[i]))

directory = "CityMapData/Durgapur"
#generateData(directory)

folders = findfiles(directory)
folders.sort()

folderLen = len(folders)

#For each bus
for ind in range(0, folderLen, 1):
    if ".DS_Store" in folders:
       print("Current Folder " + folders[ind])

    else:
        print("Bus: " + str(folders[ind]))
        folderPath = directory + "/" + str(folders[ind])
        currFiles = findfiles(folderPath)
        currFiles.sort()

        numOfFiles = len(currFiles)

        gpsFileExists = False
        for fInd in range(0, numOfFiles):

            if "GPS" in currFiles[fInd]:
                gpsFileExists = True
                filePath = folderPath + "/" + currFiles[fInd]
                file = open(filePath, "r")

                startX = 23.4945502
                startY = 87.31776490000004

                endX = 23.5651795
                endY = 87.28318239999999

                startTimes = []
                endTimes = []

                for line in file:
                    linestr = line.strip()
                    if '#' in linestr:
                        continue

                    linestr = linestr.split(",")

                    if len(linestr) > 4:
                        curTime = linestr[4]
                    else:
                        curTime = linestr[len(linestr) - 1]
                    curX = float(linestr[0])
                    curY = float(linestr[1])

                    distS = funHaversine(curX,curY,startX,startY)
                    distE = funHaversine(curX,curY,endX,endY)

                    if distS < 0.05:
                        #print("Within 100m of START at time: " + curTime)
                        startTimes.append(curTime)
                    elif distE < 0.05:
                        #print("Within 100m of END at time: " + curTime)
                        endTimes.append(curTime)

                print("START TIMES")
                printTimes(startTimes)
                print("END TIMES")
                printTimes(endTimes)
                print()
                file.close()

            # else:
            #     print("No data for this day\n")
        if gpsFileExists == False:
            print("No GPS data collected on this day\n")