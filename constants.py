#Required to generate lexington synthetic data
VMIN = 3000                    # Minimum Data Mule speed (in m/s)
VMAX = 5000                   # Maximum Data mule speed (in m/s)

# Start times may be different for different buses
route_start_time1 = 0
route_start_time2 = 15

# Simulation Time  ---- 1 plus
T = 20   # must be greater than start time
dt = 1  # this is the discrete time interval such as 0, 2, 4, 6, 8, ...
tau = 1 # Instead of looking at each dt, we would look at tau as this is the minimum time to transfer a message
# total_generation_T = 60

#TTL Bound ----  1 plus
TTL = 10
minTTL = 15
#max tau is the time taken to deliver the maximum size message over slowest band (with least bandwidth)
maxTau = 3
# Message size
M = [1, 10, 100, 1000]

V = 45         # No of nodes including source, data mules, and data centers
NoOfSources = 10
NoOfDataCenters = 5
NoOfDMs = 30                # Total number of data mules (or DSA nodes)

numSpec = 4 #always even if we only use one band

#TV ISM LTE CBRS
#3, 10, 40
minBW = [3, 8, 20, 40]               # Minimum bandwidth for each spectrum band
#6, 20, 60
maxBW = [6, 20, 30, 60]             # Maximum bandwidth for each spectrum band
#2000, 100, 500
spectRange = [2000, 500, 1500, 350]        # Transmission coverage for each spectrum band
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

lex_data_directory = 'Lexington/'
lex_data_directory_day = 'Lexington/Day1/'
link_exists_folder = 'Bands/'
path_to_folder = 'Bands/ALL/'
S = [0, 1, 2, 3]
validate_data_directory = 'Lexington/Day1/'
