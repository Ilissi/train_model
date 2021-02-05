#INPUT OF PREPROCESSING SCRIPT
#	A set of csv files with the traffic of one activity
#	A mapping file with
#		the ip of the host that generates that traffic
#		the name of the file associated
#		the activity in that file

#OUTPUT OF PREPROCESSING SCRIPT
#	A single csv with all the traffic merged
#		Each of the input files will be asociated with a unique host ip in the same net
#	A mapping file with the host ip and it's activity


#Common path to the whole proyect
main_path = '/home/vic/paper'

#Path to the modules folder. Must be a full path
MODULES_PATH = '{}/modules'.format(main_path)

#Path to the mapping file. The mapping consists in a csv with the host address, the trace name in csv and the activity
mapping_file = '{}/data/raw/mapping.csv'.format(main_path)

#Read the mapping and and generate a list with one element per data file
#Each element is a dict with the values in the csv indexed by its field name
#Lines starting with # are ignored so we can place comments in the mapping file
#TRACES = [{'host' : 192.168.1.49, 'file' : bulk_115s_01.csv, 'label' : 'bulk'}, {...}, ...]
with open(mapping_file) as f:
	header = f.readline()[:-1].split(',')
	TRACES = [{header[i] : v for i,v in enumerate(line[:-1].split(','))} for line in f if not line[0] == '#']

#Rewrite the file fields with an absolute path.
for obj in TRACES: obj['file'] = '{}/{}/{}'.format(main_path, 'data/raw/csv', obj['file'])

#Generate an array for the ip-address replacements.
#Must be at least one ip for each host to monitorize (for each data file) in the dataset
HOSTS_POOL = ['10.0.{}.{}'.format(x, y) for x in range(1, 5) for y in range(1, 100)]

#Generate another array for the others hosts in the captured dataset.
OTHERS_POOL = ['20.{}.{}.{}'.format(x, y, z) for x in range(1, 5) for y in range(1, 200) for z in range(1, 200)]

#Define the paths to the exported files of the preprocessing script
export_path = '{}/data/preprocessed'.format(main_path)
DATA_FILE = '{}/preprocessed.csv'.format(export_path)
TARGET_FILE = '{}/targetmap.csv'.format(export_path)

#Time compresion factor. Set 1 for no compression
#With a time compresion of 2. packets 1seg apart in the original file will be placed 0.5s apart
COMPRESSION_FACTOR = 1

#Enable/disable output
VERBOSE = True
