import os

number_of_runs = 1
generate_files = "Y"
# generate_files = "N"
# TODO: Generate the trajectory files
if generate_files == "Y":
    print("Generate bus trajectories ---------------------- \n")

    set_max_nodes = True
    max_nodes = 10
    src_des_nodes = 0
    run_start_time = 1

    mule_set = [10]
    simulation_times = [5]
    for max_mules in mule_set:
        for run in range(run_start_time, 2):
            for T in simulation_times:
                print("=============== Folder: Band" + str(max_mules) + " Time: " + str(T))

                #S = [0, 1, 2, 3]
                path_to_folder = "Nodes" + str(max_mules) + "/Time" + str(T) + "/Day1/ALL/XChants/"
                link_exists_folder = "Nodes" + str(max_mules) + "/Time" + str(T) + "/Day1/"
                lex_data_directory = "Lexington" + str(max_mules) + "/Time" + str(T) + "/"
                lex_data_directory_day = "Lexington" + str(max_mules) + "/Time" + str(T) + "/Day1/"
                pkl_folder = "Lexington" + str(max_mules) + "/Time_" + str(T) + "/Day1_pkl/"
                validate_pkl_folder = "Lexington" + str(max_mules) + "/Time" + str(T) + "/Day1_pkl/"


                if set_max_nodes == True:
                    # max_nodes = max_mules
                    set_max_nodes = False

                with open("Mobile/constants.py", "r") as f:
                    lines = f.readlines()

                with open("Mobile/constants.py", "w") as f:
                    for line in lines:
                        if ("path_to_folder" not in line)\
                                and ("link_exists_folder" not in line) \
                                and ("lex_data_directory" not in line) \
                                and ("V = " not in line) \
                                and ("NoOfDMs = " not in line) \
                                and ("T = " not in line) \
                                and ("max_nodes = " not in line) \
                                and ("pkl_folder" not in line):
                            f.write(line)

                    f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
                    #f.write("S = " + str(S) + "\n")
                    f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")
                    f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
                    f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
                    f.write("V = " + str(max_mules + src_des_nodes) + "\n")
                    f.write("NoOfDMs = " + str(max_mules) + "\n")
                    f.write("T = " + str(T) + "\n")
                    f.write("max_nodes = " + str(max_nodes) + "\n")
                    f.write("pkl_folder = '" + pkl_folder + "'\n")

                os.system('python3 Mobile/readLexingtonData_Fixed.py')
                os.system('python3 Mobile/create_pickles_Lex.py')
                os.system('python3 Mobile/computeLINKEXISTS_Lex.py')
