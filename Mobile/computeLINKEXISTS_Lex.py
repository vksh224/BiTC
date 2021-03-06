import pickle

from STB_help import *
from constants import *


def getIndex(ts, currTimeInFile1, currTimeInFile2, currIndexInFile1, currIndexInFile2, linesInFile1, linesInFile2):
    while currTimeInFile1 < ts and currIndexInFile1 < len(linesInFile1):
        currIndexInFile1 += 1
        currTimeInFile1 = float(linesInFile1[currIndexInFile1].split()[0])


    # # Go to ts - Skip all other lines up to ts
    while currTimeInFile2 < ts and currIndexInFile2 < len(linesInFile2):
        currIndexInFile2 += 1
        currTimeInFile2 = float(linesInFile2[currIndexInFile2].split()[0])

    return currIndexInFile1, currIndexInFile2


def CHECK_IF_LINK_EXISTS(file1_pkl, file2_pkl, s, ts, te):

    for time in range(ts, te):

        dataMule1_X = float(file1_pkl[time][0])
        dataMule1_Y = float(file1_pkl[time][1])
        dataMule2_X = float(file2_pkl[time][0])
        dataMule2_Y = float(file2_pkl[time][1])

        if dataMule1_X == -1 or dataMule2_X == -1 or dataMule1_X == '0' or dataMule2_X == '0' or dataMule1_X == ' ' or dataMule2_X == ' ':
            return False

        dist = euclideanDistance(dataMule1_X, dataMule1_Y, dataMule2_X, dataMule2_Y)

        if dist > spectRange[s]:
            return False

    return True

def createLinkExistenceADJ():
    pkl_files = []
    fileList = findfiles(pkl_folder)
    fileList.sort()



    if ".DS_Store" in fileList:
        fileList.remove(".DS_Store")
        noOfFiles = len(fileList)

    #print("Files " + str(noOfFiles), fileList)
    #print("#ts te i j s \n")

    for ts in range(0, T - dt, dt):
        for te in range(ts + dt, ts + maxTau, dt):
            for file1 in fileList:
                file1_pkl = pickle.load(open(pkl_folder + file1, "rb"))

                for file2 in fileList:
                    file2_pkl = pickle.load(open(pkl_folder + file2, "rb"))

                    for s in S:
                        if te < T:
                            ts_dt = int(ts / dt)
                            te_dt = int(te / dt)

                            file1_id = file1.split(".")[0]
                            file2_id = file2.split(".")[0]
                            # print(file1_id, file2_id)
                            if file1_id == file2_id:
                                LINK_EXISTS[int(file1_id), int(file2_id), s, ts_dt, te_dt] = 1
                            else:
                                # filepath1 = lex_data_directory_day + file1
                                # filepath2 = lex_data_directory_day + file2

                                # print("i: " + str(file1_id) + " j: " + str(file2_id) + " s: " + str(s))
                                if CHECK_IF_LINK_EXISTS(file1_pkl, file2_pkl, s, ts, te) == True:
                                    LINK_EXISTS[int(file1_id), int(file2_id), s, ts_dt, te_dt] = 1

                                  #  print("i: " + str(file1_id) + " j: " + str(file2_id) + " s: " + str(s) + " ts: " + str(ts_dt) + " te: " + str(te_dt) + " = " + str(LINK_EXISTS[int(file1_id), int(file2_id), s, ts_dt, te_dt]))

# Main starts here

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V, V, numSpec, int(T/dt), int(T/dt)))
LINK_EXISTS.fill(math.inf)

# if not os.path.exists(lex_data_directory):
#     os.makedirs(lex_data_directory)

createLinkExistenceADJ()

if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)

LE_file = open(link_exists_folder + "LINK_EXISTS.pkl", 'wb')
pickle.dump(LINK_EXISTS, LE_file, protocol = 4)
LE_file.close()

print("Size of Link Exists: " + str(len(LINK_EXISTS)) + " " + str(len(LINK_EXISTS[0])) + " " + str(len(LINK_EXISTS[0][0])) + " " + str(len(LINK_EXISTS[0][0][0])))
save_in_file(link_exists_folder + "LINK_EXISTS.txt", LINK_EXISTS)
#printMAT(LINK_EXISTS)


print("Spectrum bandwidth assigned: ")
specBW = getSpecBW(validate_data_directory, V, S, T)             # Get the dynamic spectrum bandwidth

specBW_file = open(link_exists_folder + "specBW.pkl", 'wb')
pickle.dump(specBW, specBW_file, protocol = 4)
specBW_file.close()

save_4D_in_file(link_exists_folder + "specBW.txt", specBW)
