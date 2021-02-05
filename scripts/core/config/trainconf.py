#INPUT OF THE TRAIN SCRIPT
	#The training set file generated with split.py

#OUTPUT OF THE TRAIN SCRIPT
	#A trained model stored in a file

#Common path to the whole proyect
main_path = '/home/vic/paper'

#Path to the modules folder. Must be a full path
MODULES_PATH = '{}/modules'.format(main_path)

#Path to the training dataset file
datapath =  '{}/data'.format(main_path)
TRAINING_SET = '{}/datasets/train.pickle'.format(datapath)

#Import the modules to have access to the Features class
import sys
sys.path.insert(0, MODULES_PATH)
from dataStructure import Features

#Configuration of the model
MODEL_CONFIG = {
    'layer1_features' : Features.BWindow.ALL,
    'layer1_model' : 'KMeans',
    'layer1_params' : {
        'n_clusters' : 15
    },

    'layer2_features' : Features.Flow.ALL,
    'layer2_model' : 'KMeans',
    'layer2_params' : {
        'n_clusters': 20
    },

    'layer3_features' : Features.CWindow.ALL,
    'layer3_model' : 'RF',
    'layer3_params' : {
        'n_estimators' : 1000
    }
}

#Output file where to save the trained model
MODEL_FILE = '{}/model/model.pickle'.format(datapath)

#Enable/disable output
VERBOSE = True
