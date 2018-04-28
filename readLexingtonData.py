import re
import random
import pickle

from STB_help import *

def readTrajectoryFile(DMTrajectories):
    filepath = "Lexington/primaryRoads.osm.wkt"
    with open(filepath) as fp:
        lines = fp.readlines()

        for index in range(0, len(lines)):
            patternMatch = re.match(r'^LINESTRING \((.*)\)', lines[index], re.M | re.I)

            if patternMatch:
                # print ("Pattern 1: ", patternMatch.group(1))
                trajectoryCoord = patternMatch.group(1)
                if len(trajectoryCoord.strip().split(',')) > 20:
                    DMTrajectories.append(trajectoryCoord.strip().split(','))

            else:
                print ("No Match !!!")
    fp.close()


def getSourceDesCoordinates(src_start, src_end, des_end):
    village_coors = []
    for srcID in range(src_start, des_end, 1):
        village_coors.append(random.choice(DMTrajectories[srcID % len(DMTrajectories)]))

    f = open(lex_data_directory + "village_coor.pkl", 'wb')
    pickle.dump(village_coors, f)
    f.close()

def getLocationsOfSourcesAndDataCenters(startIndex, endIndex):
    # create file for Sources. Though the source location are fixed, the spectrum bandwidth changes over time
    # Hence, it is important to save it as a file

    villageCoor = pickle.load(open(lex_data_directory + "village_coor.pkl", "rb"))
    for srcID in range(startIndex, endIndex, 1):

        # villageCoor = random.choice(DMTrajectories[srcID%len(DMTrajectories)])
        srcLocationX = villageCoor[srcID].strip().split(" ")[0]
        srcLocationY = villageCoor[srcID].strip().split(" ")[1]
        # print("Location: " + villageCoor[srcID] + " " + srcLocationX + " " + srcLocationY)

        with open(lex_data_directory_day + str(srcID) + ".txt", "w") as srcP:
            srcP.write("T X Y ")
            for s in S:
                srcP.write("S" + str(s) + " ")
            srcP.write("\n")

            for t in range(0, T, dt):
                srcP.write(str(t) + " " + str(srcLocationX) + " " + str(srcLocationY) + " ")

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [random.randrange(minBW[s], maxBW[s]) for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    srcP.write(str(sBW) + " ")
                srcP.write("\n")
        srcP.close()

def getBusRoutes(bus_start, bus_end):
    bus_routes = []
    for srcID in range(bus_start, bus_end, 1):
        bus_routes.append(random.randint(0, len(DMTrajectories)-1))

    f = open(lex_data_directory +  "bus_route_ids.pkl", 'wb')
    pickle.dump(bus_routes, f)
    f.close()
    print(bus_routes)

def getLocationsOfDMs(DMTrajectories, startIndex, endIndex):
    dmID = startIndex + NoOfSources + NoOfDataCenters - 1
    bus_route_ids = pickle.load(open(lex_data_directory + "bus_route_ids.pkl", "rb"))

    for ind in range(startIndex, endIndex, 1):
        dmID = dmID + 1
        currTime = random.randint(route_start_time1, route_start_time2)
        currCoorID = 0
        nextCoorID = 1
        dmSpeed = random.randint(VMIN, VMAX)

        # chosen_trajectory_id = random.randint(0, len(DMTrajectories)-1)

        chosen_trajectory_id  = bus_route_ids[ind]
        eachDM = DMTrajectories[chosen_trajectory_id]

        # print("Trajectory " +  str(len(eachDM)) + " : " + str(eachDM))

        with open(lex_data_directory_day + "/"+ str(dmID)+".txt", "w") as dmP:
            # print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in S:
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            # By default, move in the forward direction
            isDirectionForward = True

            for t in range(currTime, T, dt):
                prevCoors = eachDM[currCoorID].strip().split(' ')
                currCoors = eachDM[nextCoorID].strip().split(' ')

                consumedTime = euclideanDistance(prevCoors[0], prevCoors[1], currCoors[0], currCoors[1])/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))

                if consumedTime > t or t == T- dt:
                    # Stay in the same location
                    # print (str(t) + " " + str(eachDM[currCoorID]))
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")

                else:
                    # Move to the next location
                    dmP.write(str(t) + " " + eachDM[nextCoorID].strip() + " ")

                    #Set the current ID and next ID appropriately
                    currCoorID = nextCoorID

                    #repeat from start of the trajectory (if currently at the end of the trajectory)
                    # Each trajectory is periodic
                    if currCoorID == len(eachDM) - 1:
                        isDirectionForward = False

                    if currCoorID == 0:
                        isDirectionForward = True

                    if isDirectionForward:
                        nextCoorID = currCoorID + 1

                    else:
                        nextCoorID = currCoorID - 1

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [random.randrange(minBW[s], maxBW[s]) for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    dmP.write(str(sBW) + " ")
                dmP.write("\n")
        dmP.close()

# Main starts here

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V, V, numSpec, int(T/dt), int(T/dt)))
LINK_EXISTS.fill(math.inf)


if not os.path.exists(lex_data_directory_day):
    os.makedirs(lex_data_directory_day)

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(DMTrajectories)
# selectedDMTrajectories = DMTrajectories[:3]

print("Length of DM trajectories: ", len(DMTrajectories))

#TODO: Run it only for Day1

if "Day1" in lex_data_directory_day:
    getSourceDesCoordinates(0, NoOfSources, (NoOfSources +  NoOfDataCenters))
    getBusRoutes(0, NoOfDMs)

# Randomly place sources and destination nodes (index from 0 to S -1)
getLocationsOfSourcesAndDataCenters(0, NoOfSources + NoOfDataCenters)

# Place DMs on selected Routes (index from (S - DM)
getLocationsOfDMs(DMTrajectories, 0, NoOfDMs)

