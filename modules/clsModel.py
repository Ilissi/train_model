from sklearn.preprocessing import StandardScaler
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cluster import KMeans, Birch
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime as dt

SUPPORTED_MODELS = {
	#Layers 1 & 2
	'KMeans' : lambda args : KMeans(**args),
	'Birch' : lambda args : Birch(**args),
	'GM' : lambda args : GaussianMixture(**args),

	#Layer 3
	'SVM' : lambda args : OneVsRestClassifier(svm.SVC(**args)),
	'MLP' : lambda args : MLPClassifier(**args),
	'RF' : lambda args : RandomForestClassifier(**args)
}

class clsModel:
    def __init__(self, config):
        self.layer1_features = config['layer1_features']
        self.layer1_scaler = StandardScaler()
        self.k1 = config['layer1_params']['n_clusters'] if 'n_clusters' in config['layer1_params'] else config['layer1_params']['n_components']
        self.layer1_model = SUPPORTED_MODELS[config['layer1_model']](config['layer1_params'])

        # self.layer2_encoding = 'binary'
        self.layer2_features = config['layer2_features']
        self.layer2_scaler = StandardScaler()
        self.k2 = config['layer2_params']['n_clusters'] if 'n_clusters' in config['layer2_params'] else config['layer2_params']['n_components']
        self.layer2_model = SUPPORTED_MODELS[config['layer2_model']](config['layer2_params'])

        # self.layer3_encoding = 'binary'
        self.layer3_features = config['layer3_features']
        self.layer3_scaler = StandardScaler()
        self.layer3_model = SUPPORTED_MODELS[config['layer3_model']](config['layer3_params'])

    def pull_layer1(self, w1_arr):
        data = []
        for clsWindow in w1_arr:
            for flowkey, flowStruct in clsWindow.flows.items():
                for behavWindow in flowStruct.windows:
                    tmp = behavWindow.export_features(f = self.layer1_features)
                    if tmp is not None: data.append(tmp)
        return data
    def set_layer1(self, w1_arr, w2_pred):
        index = 0
        for clsWindow in w1_arr:
            for flowkey, flowStruct in clsWindow.flows.items():
                for behavWindow in flowStruct.windows:
                    tmp = behavWindow.export_features(f = self.layer1_features)
                    if tmp is not None:
                        behavWindow.set_cluster(w2_pred[index] + 1)
                        index += 1
                    else: behavWindow.set_cluster(0)

    def pull_layer2(self, w1_arr):
        data = []
        for clsWindow in w1_arr:
            for flowkey, flowStruct in clsWindow.flows.items():
                binary_encoding = [0] * (self.k1 + 1)
                for bw in flowStruct.windows: binary_encoding[bw.cluster] = 1
                data.append(flowStruct.export_features(f = self.layer2_features) + binary_encoding)
        return data
    def set_layer2(self, w1_arr, flow_pred):
        index = 0
        for clsWindow in w1_arr:
            for flowkey, flowStruct in clsWindow.flows.items():
                flowStruct.set_cluster(flow_pred[index])
                index += 1

    def pull_layer3(self, w1_arr):
        data = {'x' : [], 'y' : []}
        for clsWindow in w1_arr:
            binary_encoding = [0] * self.k2
            for flow in clsWindow.flows.values(): binary_encoding[flow.cluster] = 1
            data['x'].append(clsWindow.export_features(f = self.layer3_features) + binary_encoding)
            data['y'].append(clsWindow.target)
        return data

    def train(self, w1_arr):
        layer1_in = self.pull_layer1(w1_arr)
        self.layer1_scaler.fit(layer1_in)
        self.layer1_model.fit(self.layer1_scaler.transform(layer1_in))
        self.set_layer1(w1_arr, self.layer1_model.predict(self.layer1_scaler.transform(layer1_in)))

        layer2_in = self.pull_layer2(w1_arr)
        self.layer2_scaler.fit(layer2_in)
        self.layer2_model.fit(self.layer2_scaler.transform(layer2_in))
        self.set_layer2(w1_arr, self.layer2_model.predict(self.layer2_scaler.transform(layer2_in)))

        layer3_in = self.pull_layer3(w1_arr)
        self.layer3_scaler.fit(layer3_in['x'])
        self.layer3_model.fit(self.layer3_scaler.transform(layer3_in['x']), layer3_in['y'])


    def test(self, w1_arr):
        self.set_layer1(w1_arr, self.layer1_model.predict(self.layer1_scaler.transform(self.pull_layer1(w1_arr))))
        self.set_layer2(w1_arr, self.layer2_model.predict(self.layer2_scaler.transform(self.pull_layer2(w1_arr))))
        layer3_in = self.pull_layer3(w1_arr)
        layer3_pred = self.layer3_model.predict(self.layer3_scaler.transform(layer3_in['x']))
        return [{'target' : layer3_in['y'][i], 'pred' : layer3_pred[i]} for i in range(len(layer3_pred))]
