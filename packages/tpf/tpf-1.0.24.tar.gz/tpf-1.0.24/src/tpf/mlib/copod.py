



import pandas as pd 
import numpy as np 
import joblib
from pyod.models.copod import COPOD
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PowerTransformer

class COPODModel():
    def __init__(self, contamination=0.05):
        """
        
        """
        self.contamination = contamination 

    def predict_proba(self, X):
        model = COPOD(contamination=self.contamination)
        model.fit(np.array(X))
        scaler = MinMaxScaler()
        copod_scores_2d = model.decision_scores_.reshape(-1,1)
        
        # 分数进行box-cox转换
        pt = PowerTransformer(method = 'box-cox')
        copod_scores_i_boxcox = pt.fit_transform(copod_scores_2d)
        
        copod_scores_nol = scaler.fit_transform(copod_scores_i_boxcox).flatten()
        return copod_scores_nol
    


exampel = """

from sklearn.preprocessing import StandardScaler
def generate_data(n_normal=100, n_anomalies=10):
    normal_data = np.random.normal(loc=0, scale=1, size=(n_normal, 2))
    anomaly_data = np.random.normal(loc=5, scale=0.5, size=(n_anomalies, 2))
    return np.vstack((normal_data, anomaly_data))

data = generate_data()

# 数据预处理（标准化）
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)


model = COPODModel()

model.predict_proba(X = data_scaled)

"""