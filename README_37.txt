Usage of the code:

#<-- CHECK DEPENDENCIES
-Step 0: Check linux and python dependencies with scripts/helper/checkdependencies.py
	This script supports -h option
#-->

#<-- CAPTURE FOLDER
- Step 1: Capture the traffic pcaps
	Use the capturepcap.sh script. Example using the -h option

- Step 2: Parse pcap to csv
	Use pcap2csv.py or pcap2csv.sh
	scripts/capture/pcap2csv.py : Parses one file. Example using the -h option
	scripts/helper/pcap2csv.sh : Parses all the pcaps in a folder using the python script. Example in the help
#-->

#<-- CORE FOLDER
- Step 3: Perform the data preprocessing
	Use the scripts/core/preprocessing.py script.

	3.1 : Modify the scripts/core/config/preprocessingconf.py according to your requirements
		(lowercase variables are not required to be set)
	3.2 : Run the preprocessing.py script using the absolute path to the config as argument

- Step 4: Perform the data restructuration
	Use the scripts/core/restructure.py script.

	4.1 : Modify the scripts/core/config/restructureconf.py according to your requirements
		(lowercase variables are not required to be set)
	4.2 Run the restructure.py script using the absolute path to the config as argument

- Step 5: Perform the data train-test split
	Use the scripts/core/split.py script.

	5.1 : Modify the scripts/core/config/splitconf.py according to your requirements
		(lowercase variables are not required to be set)
	5.2 : Run the split.py script using the absolute path to the config as argument

- Step 6: Perform the traning of the model
	Use the scripts/core/train.py script.

	6.1 : Modify the scripts/core/config/trainconf.py according to your requirements
		(lowercase variables are not required to be set)
	6.2 : Run the train.py script using the absolute path to the config as argument

- Step 7: Perform the testing of the model
	Use the scripts/core/test.py script

	7.1 : Modify the scripts/core/config/testconf.py according to your requirements
		(lowercase variables are not required to be set)
	7.2 : Run the test.py script using the absolute path to the config as argument


- Steps 5,6,7 in one: Train-test split & training & testing
	Use the scripts/helper/traintest.py script

	Modify the config file from steps 5.1, 6.1 & 7.1
	Run traintest.py using the absolute paths to the config files and scripts. Example using the -h option
#-->
