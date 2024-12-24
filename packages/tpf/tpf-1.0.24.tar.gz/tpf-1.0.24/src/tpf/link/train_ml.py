

import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

from tpf.link.toolml import pkl_load,pkl_save
from tpf.datasets import pd_ruxianai
from tpf.mlib.copod import COPODModel



class MLib():
    
    @staticmethod
    def copod_base_line(contamination=0.05):
        model = COPODModel(contamination=0.05)
        return model 
    
    @staticmethod
    def lgbm_params():
        params = """
                
        # 设置LightGBM参数
        params = {
            'objective': 'binary',  # 目标函数为二分类
            'metric': 'auc',  # 评估指标为AUC
            'max_depth': 6,  # 树的最大深度
            'num_leaves': 31,  # 叶子节点数
            'learning_rate': 0.02,  # 学习率
            'bagging_fraction': 0.8,  # 每次迭代时用的数据比例
            'bagging_freq':3,
            'feature_fraction': 0.8,  # 每次迭代中随机选择特征的比例
            'min_child_samples':3,  # 一个叶子节点上数据的最小数量
            'min_data_in_leaf':100,
            'verbose': -1,  # 是否打印训练过程中的信息，-1表示不打印
            'max_bin':3,
            'min_gain_to_split':0,
            'min_data_in_leaf':10,
            'force_col_wise':True
        }
        ## num_boost_round
        -提升算法是一种集成学习技术，它通过结合多个弱学习器（通常是决策树）来形成一个强学习器。
        -每一轮（round）中，算法都会根据当前模型的预测误差来构建一个新的弱学习器，
        -并将其添加到已有的模型集合中，以此来减少总体误差。
        -num_boost_round参数指的是算法将执行的提升（boosting）轮次的数量。
        -
        简单说，就是num_boost_round控制了lightgbm训练的轮次
        ## min_data_in_leaf
        - 默认是20，减少这个值可以让模型在叶子节点中包含更少的数据点，这有助于在数据较少的情况下进行分裂。
        - 因样本数据非常少的情况下，可以适当降低这个值
        ## force_col_wise
        - 在内存不足的情况下，force_col_wise为True，有助于模型训练
        ## max_bin
        - 每个特征 最多 划分为多少个箱子
        - 模型只是参考用户所输入的参数，具体如何分箱，全体数据集划分多少个箱子，仍以模型的自我决定为主
        - 这个参数通常是先让模型自主决定，出现问题时再人工介入调整
        ## max_depth
        －　default = -1, type = int
            limit the max depth for tree model. 
            This is used to deal with over-fitting when #data is small. 
            Tree still grows leaf-wise
            <= 0 means no limit
        - 决策树划分时，从root节点开始，到叶子节点分支上的节点个数，为树的深度(depth)，
        - 叶子节点存储的是分类结果，不再划分数据,比如min_data_in_leaf参数可以确定一个叶子最多存储多少个数据
        - 如果只有一次划分，就是一个root节点，加上两个叶子节点，此时的depth为1,max_depth亦为1
        - 有多个分支时，max_depth是所有分支中最大的depth

        ## num_leaves 
        - max number of leaves in one tree
        - default = 31, 
        - type = int, 
        - aliases: num_leaf, max_leaves, max_leaf, max_leaf_nodes, 
        - constraints: 1 < num_leaves <= 131072
        - 影响模型复杂度和拟合能力
        ## feature_fraction 
        -当设置 feature_fraction=0.9 时，它意味着在构建每一棵树时，
        -算法会随机选择大约90%的特征来进行树的分裂操作，而不是全部特征。
        ## bagging_fraction与bagging_freq
        - 当 `bagging_fraction=0.9` 时，表示每次构建树模型时将从原始训练数据集中随机抽取 90% 的数据样本用于训练该树。这种做法可以增加模型的多样性，并有助于提高模型的泛化能力。
        - `bagging_freq` 指定每多少次迭代执行一次 bagging（数据采样）操作。例如，如果 `bagging_freq=2`，则表示每两次迭代执行一次 bagging。
        ## max_bin
        - 每个特征 最多 划分为多少个箱子
        - 模型只是参考用户所输入的参数，具体如何分箱，全体数据集划分多少个箱子，仍以模型的自我决定为主
        - 这个参数通常是先让模型自主决定，出现问题时再人工介入调整

        """
        return params 
    
    @staticmethod 
    def lgbm1(X_train, y_train,X_test, y_test):
        """
        params = {
            'objective': 'binary',  # 目标函数为二分类
            'metric': 'auc',  # 评估指标为AUC
            'num_leaves': 31,  # 叶子节点数
            'max_depth': 6,  # 树的最大深度
            'learning_rate': 0.02,  # 学习率
            'bagging_fraction': 0.8,  # 每次迭代时用的数据比例
            'feature_fraction': 0.8,  # 每次迭代中随机选择特征的比例
            'min_child_samples': 25,  # 一个叶子节点上数据的最小数量
            'verbose': -1  # 是否打印训练过程中的信息，-1表示不打印
        }

        # 训练LightGBM模型
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], 
                eval_metric=['auc', 'binary_logloss'])
        
        """
        # 设置LightGBM参数
        params = {
            'objective': 'binary',  # 目标函数为二分类
            'metric': 'auc',  # 评估指标为AUC
            'boosting_type': 'gbdt',
            'num_leaves': 31,  # 叶子节点数
            'max_depth': 6,  # 树的最大深度
            'learning_rate': 0.02,  # 学习率
            'bagging_fraction': 0.8,  # 每次迭代时用的数据比例
            'feature_fraction': 0.8,  # 每次迭代中随机选择特征的比例
            'min_child_samples': 25,  # 一个叶子节点上数据的最小数量
            'verbose': -1  # 是否打印训练过程中的信息，-1表示不打印
        }

        # 训练LightGBM模型
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], 
                eval_metric=['auc', 'binary_logloss'])
        return model 
    
    @staticmethod
    def lgbm2(X_train, y_train,X_test, y_test, cat_features,num_boost_round,params=None):
        """
        # free_raw_data=False是因为在数据上设置部分列为category类型,此时lightgbm要求这个数据集不能被释放
        train_data = lgb.Dataset(X_train, label=y_train, free_raw_data=False, categorical_feature=cat_features)
        test_data = lgb.Dataset(X_test, label=y_test,  reference=train_data)

        # 设置参数并训练模型
        if params is None:
            params = {
                'objective': 'binary', 
                'metric': 'binary_logloss', 
                'boosting_type': 'gbdt',
                'max_depth': 3,
                'num_leaves': 3,
                'max_bin':3,
                'min_gain_to_split':0,
                'min_data_in_leaf':10,
                'force_col_wise':True}
        lgb_model = lgb.train(params, train_data, num_boost_round=num_boost_round,  valid_sets=[test_data],)
        
        """
        # 创建LightGBM数据集，并指定分类特征
        # free_raw_data=False是因为在数据上设置部分列为category类型,此时lightgbm要求这个数据集不能被释放
        train_data = lgb.Dataset(X_train, label=y_train, free_raw_data=False, categorical_feature=cat_features)
        test_data = lgb.Dataset(X_test, label=y_test,  reference=train_data)

        # 设置参数并训练模型
        if params is None:
            params = {
                'objective': 'binary', 
                'metric': 'binary_logloss', 
                'boosting_type': 'gbdt',
                'max_depth': 3,
                'num_leaves': 3,
                'max_bin':3,
                'min_gain_to_split':0,
                'min_data_in_leaf':10,
                'force_col_wise':True}
        lgb_model = lgb.train(params, train_data, num_boost_round=num_boost_round,  valid_sets=[test_data],)
        return  lgb_model
     
    @staticmethod
    def lgbm_baseline(X_train, y_train,X_test, y_test, cat_features,num_boost_round,params=None):
        """
        # 创建LightGBM数据集，并指定分类特征
        # free_raw_data=False是因为在数据上设置部分列为category类型,此时lightgbm要求这个数据集不能被释放
        train_data = lgb.Dataset(X_train, label=y_train, free_raw_data=False, categorical_feature=cat_features)
        test_data = lgb.Dataset(X_test, label=y_test,  reference=train_data)

        # 设置参数并训练模型
        if params is None:
            params = {
                'objective': 'binary', 
                'metric': 'binary_logloss', 
                'boosting_type': 'gbdt',
                'force_col_wise':True}
        lgb_model = lgb.train(params, train_data, num_boost_round=num_boost_round,  valid_sets=[test_data],)
        
        """
        # 创建LightGBM数据集，并指定分类特征
        # free_raw_data=False是因为在数据上设置部分列为category类型,此时lightgbm要求这个数据集不能被释放
        train_data = lgb.Dataset(X_train, label=y_train, free_raw_data=False, categorical_feature=cat_features)
        test_data = lgb.Dataset(X_test, label=y_test,  reference=train_data)

        # 设置参数并训练模型
        if params is None:
            params = {
                'objective': 'binary', 
                'metric': 'binary_logloss', 
                'boosting_type': 'gbdt',
                'force_col_wise':True}
        lgb_model = lgb.train(params, train_data, num_boost_round=num_boost_round,  valid_sets=[test_data],)
        return  lgb_model

    @staticmethod
    def model_save(model,model_path):
        pkl_save(model,file_path=model_path,use_joblib=True)
    
    @staticmethod
    def lr_base_line(X_train, y_train, max_iter=10000):
        label = np.array(y_train)
        if label.ndim >1:
            label = label.ravel()  #转换为一维数组

        # 初始化逻辑回归模型
        lr = LogisticRegression(max_iter=max_iter)  # 增加迭代次数以确保收敛

        # 训练模型
        lr.fit(X_train, label)
        return lr  
    
    @staticmethod
    def model_load(model_path):
        model = pkl_load(file_path=model_path,use_joblib=True)
        return model  
    
    @staticmethod
    def lgbm_cv1(train_data, num_boost_round=1, nfold=3):
        """交叉验证示例
        """
        # 设置参数并训练模型
        params = {
            'objective': 'binary', 
            'metric': 'binary_logloss', 
            'boosting_type': 'gbdt',
            'max_depth': 3,
            'num_leaves': 3,
            'min_gain_to_split':0,
            'min_data_in_leaf':10,
            'force_col_wise':True}
        cv_results = lgb.cv(params, train_data, num_boost_round=num_boost_round,  nfold=3, stratified=True, metrics=['binary_logloss'])
        return cv_results
    
    @staticmethod
    def svc_base_line(X_train, y_train, C=1.0):
        label = np.array(y_train)
        if label.ndim >1:
            label = label.ravel()  #转换为一维数组
        # 训练SVC模型，并设置probability=True以生成预测概率
        svc = SVC(kernel='rbf', gamma='auto', C=C, probability=True)
        svc.fit(X_train, label)
        return svc 
    
    
    
    
    
        
    
class Link():

    def __init__(self, *args, **kwargs):
        """训练步骤/流程
        
        """
        # super(CLASS_NAME, self).__init__(*args, **kwargs)
        pass
        
    @staticmethod
    def a_readdata(file_path, split_flag=None):
        """第一步：读取数据，返回pandas数表及三种字段类型
        
        params:
        ----------------------
        - file_path: 训练所需要的数据集文件
        - split_flag: 拆分文件中一行数据的字符
        
        return
        ----------------------
        - 数据集df
        - 三类字段字段，标识，数字，布尔
        
        examples
        -----------------------------------------
        
        """
        # 读取数据 
        # df = pd_ruxianai(file_path)
        df = pd.read_csv(file_path)

        return df

    
    



class ModelPre():
    """模型预测
    - 统计由predict_probs方法实现
    - 无此方法的，通过添加方法转化为该方法，目前只有lightgbm出现了无此API的情况
    """
    
    @classmethod
    def predict_proba(cls, data, model_path=None, model_type=None):
        """根据模型的路径加载模型，然后预测
        - model_type: 可选参数有["lgbm",None]，即是lgbm or 不是
        
        """
        y_probs = []
        if model_type is None:
            y_probs = cls.cls2_predict_proba(data,model_path=model_path)
        elif model_type=="lgbm":
            y_probs = cls.lgbm_predict_proba(data,model_path=model_path)
        else: # 二分类，概率返回
            y_probs = cls.cls2_predict_proba(data,model_path=model_path)
            
        if len(y_probs)>0 and isinstance(y_probs[0],np.int64):
            raise Exception(f"期望返回浮点型概率，但目前返回的是Int64类型的标签:{y_probs[0]}")
        return y_probs 
        
    @classmethod
    def lgbm_predict_proba(cls, data, model_path=None):
        """二分类问题
        """
        model_lgbm = MLib.model_load(model_path=model_path)
        y_porbs = model_lgbm.predict(data) 
        return y_porbs


    @classmethod
    def cls2_predict_proba(cls, data, model_path=None):
        """二分类问题
        - 适用返回2列概率的场景，包括深度学习
        """
        model = MLib.model_load(model_path=model_path)
        y_porbs = model.predict_proba(data) 
        if isinstance(y_porbs,np.ndarray) and y_porbs.ndim == 1:
            return y_porbs
        return y_porbs[:,1]
        
