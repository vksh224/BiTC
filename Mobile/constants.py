#Required to generate lexington synthetic data

# Start times may be different for different buses
route_start_time1 = 0
route_start_time2 = 0

# Simulation Time  ---- 1 plus
dt = 1  # this is the discrete time interval such as 0, 2, 4, 6, 8, ...
tau = 1 # Instead of looking at each dt, we would look at tau as this is the minimum time to transfer a message

#TTL Bound ----  1 plus
TTL = 1
minTTL = 15
#max tau is the time taken to deliver the maximum size message over slowest band (with least bandwidth)
maxTau = 5
# Message size
M = [100]

numSpec = 1 #always even if we only use one band

#TV ISM LTE CBRS
#3, 10, 40
minBW = [6, 10, 20, 40]               # Minimum bandwidth for each spectrum band
#6, 20, 60
maxBW = [6, 20, 30, 60]             # Maximum bandwidth for each spectrum band
#2000, 100, 500
#spectRange = [4200, 500, 2300, 700]
spectRange = [1800, 450, 1200, 350]        # Transmission coverage for each spectrum band
# specRange = [1, 2, 0.5]
spectPower = [4, 1, 4, 10]          # Transmission power for each spectrum band

epsilon = 0.5             #energy consumed in temporal link

#Channel sensing, transmission, spectrum handoff
t_sd = 0.16   #in minutes - 10s
t_td = 0.5     #in minutes - 30s
idle_channel_prob = 0.5

switching_delay = 0.001 #in joules
sensing_power = 0.04 #in Watts

#Message generation
lambda_val = 1   #lambda in exponential function
messageBurst = [2, 5]
StartTime = 0

validate_data_directory = 'Lexington/Day1/'
delivery_file_name = "delivery_day1.txt"
metrics_file_name = "metrics_LLC_day1.txt"
VMIN = 400
VMAX = 600
wait_time = [2, 7]
run_start_time = 1
S = [0]
path_to_folder = 'Nodes10/Time15/Day1/ALL/XChants/'
link_exists_folder = 'Nodes10/Time15/Day1/'
lex_data_directory = 'Lexington10/Time15/'
lex_data_directory_day = 'Lexington10/Time15/Day1/'
V = 10
NoOfDMs = 10
T = 15
max_nodes = 10
pkl_folder = 'Lexington10/Time_15/Day1_pkl/'
