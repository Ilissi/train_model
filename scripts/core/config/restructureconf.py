#INPUT OF THE RESTRUCTURE SCRIPT
#	Both output files from preprocessing.py

#OUTPUT OF RESTRUCTURE SCRIPT
#	A single binary file storing the whole dataset
#		in the hierarchical window structure


#Common path to the whole proyect
main_path = '/home/vic/paper'

#Path to the modules folder. Must be a full path
MODULES_PATH = '{}/modules'.format(main_path)

#Paths to the csv traffic and mapping files generated with preprocessing.py
datapath =  '{}/data'.format(main_path)
TRAFFIC_FILE = '{}/preprocessed/preprocessed.csv'.format(datapath)
TARGETMAP_FILE = '{}/preprocessed/targetmap.csv'.format(datapath)

#Regex to decide whether or not the host is from the monitoring net
#We are only monitoring traffic from hosts in that net
#MUST MATCH THE NET GENERATED FOR HOSTS_POOL IN preprocessingconf.py
CAPTURE_NET = '^10\\.0\\.\\d{1,3}\\.\\d{1,3}'

#CW and BW sizes in seconds. In some modules they are also called w1 and w2 respectively
CW_length = 5.0
BW_length = 0.5

#Path to the restructured dataset file
RESTRUCTURED_FILE = '{}/restructured/restructured.pickle'.format(datapath)

#Enable/disable output
VERBOSE = True
