import pickle
import random
import re
from shutil import copyfile

from STB_help import *
from constants import *


def readTrajectoryFile(DMTrajectories):
    filepath = "Lexington/primaryRoads.osm.wkt"
    with open(filepath) as fp:
        lines = fp.readlines()

        for index in range(0, len(lines)):
            patternMatch = re.match(r'^LINESTRING \((.*)\)', lines[index], re.M | re.I)

            if patternMatch:
                #print ("Pattern 1: ", patternMatch.group(1))
                trajectoryCoord = patternMatch.group(1)
                if len(trajectoryCoord.strip().split(',')) > 40:
                    DMTrajectories.append(trajectoryCoord.strip().split(','))

            else:
                print ("No Match !!!")
    fp.close()

def getBusRoutes(bus_start, bus_end):
    bus_routes = []
    for srcID in range(bus_start, bus_end, 1):
        bus_routes.append(random.randint(0, len(DMTrajectories)-1))

    f = open(lex_data_directory +  "bus_route_ids.pkl", 'wb')
    pickle.dump(bus_routes, f)
    f.close()
    print(bus_routes)

def getLocationsOfDMs(DMTrajectories, startIndex, endIndex):
    dmID = - 1
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


        with open(lex_data_directory_day + "/"+ str(dmID)+".txt", "w") as dmP:
            # print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in S:
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            # By default, move in the forward direction
            isDirectionForward = True

            chosen_wait_time = random.choice(wait_time)

            for t in range(currTime, T, dt):
                prevCoors = eachDM[currCoorID].strip().split(' ')
                currCoors = eachDM[nextCoorID].strip().split(' ')

                consumedTime = euclideanDistance(prevCoors[0], prevCoors[1], currCoors[0], currCoors[1])/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))


                # if prevCoors in villageCoor:
                if chosen_wait_time > 0:
                    chosen_wait_time -= 1
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")
                    # if chosen_wait_time == 1:
                    #     print("Bus ", chosen_trajectory_id, " Time: " , t, " Coor: ", prevCoors, " Cons Time: ", consumedTime)

                elif consumedTime > t or t == T- dt:
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
                specBW = [minBW[s] for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    dmP.write(str(sBW) + " ")
                dmP.write("\n")
        dmP.close()

# Main starts here

#We want same source, destination, and bus routes irrespective of number of runs and days
lex_data_directory = lex_data_directory.split("/")[0] +"/" + lex_data_directory.split("/")[1] + "/"

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V, V, numSpec, int(T/dt), int(T/dt)))
LINK_EXISTS.fill(math.inf)

T = T + 10

if not os.path.exists(lex_data_directory_day):
    os.makedirs(lex_data_directory_day)

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(DMTrajectories)
# selectedDMTrajectories = DMTrajectories[:3]

print("Length of DM trajectories: ", len(DMTrajectories))

print("New locations generated\n")

getBusRoutes(0, V)

# Place DMs on selected Routes (index from (S - DM)
getLocationsOfDMs(DMTrajectories, 0, V)
