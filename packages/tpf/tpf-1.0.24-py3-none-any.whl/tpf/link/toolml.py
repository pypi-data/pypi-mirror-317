import numpy as np 
import pandas as pd 
import joblib 
import pickle as pkl 
import os
import random 
import lightgbm as lgb
from sklearn.metrics import accuracy_score,roc_auc_score, confusion_matrix, classification_report, roc_curve, auc,f1_score
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


class Corr():
    def __init__(self,X,corr_line=0.95):
        """使用pandas中的corr方法计算特征相关性
        - X:pandas数表
        - corr_line:相关性阈值
        """
        # 计算特征之间的相关系数矩阵
        self.corr_matrix = X.corr()
        self.corr_line = corr_line
        self.columns = X.columns.tolist()

    def pairs(self):
        """展示任何两列之间的相关性
        - 'col1', 'col2', 'correlation'
        """
        # 创建一个空的DataFrame来存储两两特征之间的相关性
        corr_pairs = pd.DataFrame(columns=['col1', 'col2', 'correlation'])
        
        # 遍历相关系数矩阵的上三角（不包括对角线），记录特征对及其相关性
        col_num = len(self.corr_matrix.columns)
        for i in range(col_num):
            for j in range(i + 1, col_num):
                if corr_pairs.shape[0] == 0:
                    corr_pairs =  pd.DataFrame({
                    'col1': self.corr_matrix.columns[i],
                    'col2': self.corr_matrix.columns[j],
                    'correlation': self.corr_matrix.iloc[i, j]
                }, index=[0],columns=['col1', 'col2', 'correlation'])
                else:
                    corr_pairs_new = pd.DataFrame({
                        'col1': self.corr_matrix.columns[i],
                        'col2': self.corr_matrix.columns[j],
                        'correlation': self.corr_matrix.iloc[i, j]
                    }, index=[0], columns=['col1', 'col2', 'correlation'])
                    corr_pairs = pd.concat([corr_pairs, corr_pairs_new], ignore_index=True)
        return corr_pairs


    def high_mat(self):
        """高度相关列矩阵
        """
        # 找出相关性大于corr_line的特征对  
        high_correlation_pairs = self.corr_matrix[(self.corr_matrix > self.corr_line) & (self.corr_matrix.ne(1.0))]  
        high_correlation_pairs=high_correlation_pairs.fillna(0)
        return high_correlation_pairs

    def drop_list(self):
        """高度相关且可删除的特征名称
        - 两列相关，保留第一个特征
        """
        high_correlation_pairs = self.high_mat()
        # 遍历高相关性对，只保留其中一个特征  
        # 注意：这里假设我们总是保留第一个特征（可以根据实际情况调整）  
        features_to_drop = []  
        for index, row in high_correlation_pairs.iterrows():  
            for col in row.index[row > self.corr_line]:  
                if index < col:  # 确保我们不会重复删除（只考虑上三角或下三角）  
                    features_to_drop.append(col)  
        return list(set(features_to_drop))
    def new_list(self):
        """线性相关选择特征列
        - 去除相关性高的列之后剩下的特征列
        """
        _list = set(self.columns) - set(self.drop_list()) 
        return list(_list)
        

    def high_pairs(self,feature_name=None):
        """查看与feature_name高度相关的特征有哪些
        - feature_name：数据集中的特征名称，若不输入具体某个特征，则输出所有相关性高的特征对
        """
        corr_pairs = self.pairs()
        if feature_name is None:
            df1 = corr_pairs[corr_pairs["correlation"]>self.corr_line]
        else:
            #查询所要删除的列中的特征与哪些特征高度相关
            df1 = corr_pairs[corr_pairs["col1"].eq(feature_name)]
            df1 = df1[df1["correlation"]>self.corr_line]
        return df1.sort_values(by='correlation', ascending=False)
        


class FeatureEval(Corr):
    def __init__(self, X=None, corr_line=None,):
        """
        - model:树模型，如果为None则使用方法内部的模板

        examples
        ---------------------------------------
        fe = FeatureEval(X, y, num_boost_round=3)
        fe.important_features()  #特征特征重要性
        
        fe = FeatureEval(X, corr_line=0.95)
        fe.high_pairs()          #高相关性特征对
        fe.high_pairs(feature_name="mean radius") #获取指定特征的高度相关的特征对
        fe.pairs()               # 所有特征的相关性关系对
        fe.new_list()    # 去除高度相关性之后的特征列表
        
        """
        if corr_line is not None and X is not None:
            super().__init__(X,corr_line=corr_line)
  
    def important_features(self, X, y, model=None, num_boost_round=100):
        if model is None:
            if y.dtype !="int64": #分类问题，标签为整数 
                y = y.astype(np.int64)
            # 创建LightGBM数据集
            train_data = lgb.Dataset(X, label=y)
            
            # 设置参数
            params = {
                'objective': 'binary',
                'metric': 'binary_logloss',
                'boosting_type': 'gbdt'
            }
            
            # 训练模型
            model = lgb.train(params, train_data, num_boost_round=num_boost_round)
        else:
            model = model 

        # 获取特征重要性
        importance = model.feature_importance()
        feature_names = X.columns
    
        # 创建特征重要性的DataFrame
        important_features = pd.DataFrame({'feature': feature_names, 'importance': importance})
        
        # 按重要性排序
        self._important_features = important_features.sort_values(by='importance', ascending=False)
        
        return self._important_features
        
    def n_important_features(self, X, y, model=None, num_boost_round=100, n=200, is_more_than_zero=True):
        """前n个重要特征
        
        params
        ---------------------------------------------
        - num_boost_round:训练的轮次
        - n:取前n个重要特征
        - is_more_than_zero:是否只保留重要生大于0的特征
        
        return
        ---------------------------------
        - 前n个重要特征列表
        """
        seature_by_importance = self.important_features(X,y,model=model, num_boost_round=num_boost_round)
        if is_more_than_zero:
            seature_by_importance=seature_by_importance[seature_by_importance['importance'] >0]
        i_list = seature_by_importance[:n]['feature'].tolist()
        return i_list
    
    def pd_important_features(self, X, y, model=None, num_boost_round=100, n=200, is_more_than_zero=True):
        """前n个重要特征
        
        params
        ---------------------------------------------
        - num_boost_round:训练的轮次
        - n:取前n个重要特征
        - is_more_than_zero:是否只保留重要生大于0的特征
        
        return
        ---------------------------------
        - 前n个重要特征列表
        """
        seature_by_importance = self.important_features(X,y,model=model, num_boost_round=num_boost_round)
        if is_more_than_zero:
            seature_by_importance=seature_by_importance[seature_by_importance['importance'] >0]
        i_list = seature_by_importance[:n]
        return i_list
        
class ModelEval():
    def __init__(self):
        pass
    
    @staticmethod
    def evaluate(y_probs, y_test):
        """模型评估
        params
        -------------------------------------------------------
        - y_probs:模型概率输出,1维，每个元素为 标签1的概率，即正样本概率列表
        - y_test:真实标签，1维
        
        return
        -------------------------
        - acc,precision,recall,f1,auc ,依次为准确率，精确率，召回率，f1值，AUC 
        - 其中精确率，召回率只针对 正样本-1
        
        examples
        --------------------------------------------------------
        acc,precision,recall,f1,auc  = me.evaluate(y_probs,y_test)
        """
        return model_evaluate(y_probs,y_test)
    
    @staticmethod
    def confusion_matrix(y_probs, y_test):
        """
                    pre
                    0  1 
        real    0
                1 
        """
        if y_probs.ndim !=1:
            raise Exception(f"y_probs必须为1维，实际为{y_probs.ndim }维")
        # 定义预测结果：概率>0.5则预测结果为 1 即可疑；概率<=0.5则预测结果为0 即不可疑
        y_pred = np.where(y_probs>0.5,1,0)
        is_single_value = is_single_label(y_test, y_pred)
        if is_single_value:
            roc_auc = 1
        else:
            # auc = roc_auc_score(y_test, y_pred)
            # 计算ROC曲线和AUC值
            fpr, tpr, thresholds = roc_curve(y_test, y_probs)
            roc_auc = auc(fpr, tpr)
        
        print("label value count:\n",y_test.value_counts())
        conf_matrix = confusion_matrix(y_test, y_pred)
        return conf_matrix
    
    @staticmethod
    def classification_report(y_probs, y_test):
        y_pred = np.where(y_probs>0.5,1,0)
        report = classification_report(y_test, y_pred)
        return report

def random_str(seq_len=(1,3)):
    """随机生成seq_len[0]到 seq_len[1]长度的字符串
    - 字符串由字母与数字组成
    """
    # 单词集合，对应键盘上的字母
    words = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
        'q', 'w', 'e', 'r',  't', 'y',  'u', 'i', 'o', 'p', 
        'a', 's', 'd', 'f',  'g', 'h',  'j', 'k', 'l', 
        'z', 'x', 'c', 'v',  'b', 'n',  'm'
    ]
        
    # 每个词被选中的概率，随机初始化的概率
    p = np.array([
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
        1,   2,  3,  4,  5,  6,  7,  8,  9, 10, 
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
    ])
    
    # 转概率，所有单词的概率之和为1
    p = p / p.sum()
    
    # 随机选n个词
    # Return random integer in range [a, b], including both end points.
    n = random.randint(seq_len[0], seq_len[1])
    x = np.random.choice(words, size=n, replace=True, p=p)
    return "".join(x)

def random_str_list(n=5,seq_len=(1,3)):
    """生成字符串列表
    """
    tmp = []
    for i in range(n):
        tmp.append(random_str(seq_len))
    return tmp 


def pkl_save(data, file_path, use_joblib=False, compress=0):
    """
    data:保存一个列表时直接写列表,多个列表为tuple形式
    """
    if use_joblib:
        joblib.dump(data, filename=file_path, compress=compress)
    else:
        data_dict = {}
        if type(data).__name__ == 'tuple':
            index = 0
            for v in data:
                index = index+1
                key = "k"+str(index)
                data_dict[key]= v 
        else:
            data_dict["k1"] = data 

        # 在新文件完成写入之前，不要损坏旧文件
        tmp_path = file_path+".tmp"
        bak_path = file_path+".bak"

        with open(tmp_path, 'wb') as f:
            # 如果这一步失败，原文件还没有被修改，重新写入即可
            pkl.dump(data_dict, f)

            # 如果这一步失败，.tmp文件已经被成功写入，直接将.tmp去掉就是最新写入的文件
            # 这里并没有测试rename是否被修改文件的内容，从命名上看，rename是不会的，
            if os.path.exists(file_path):
                os.rename(src=file_path,dst=bak_path)
        if os.path.exists(tmp_path):
            # 如果是下面这一步被强制中止，直接将.tmp去掉就是最新写入的文件
            # 也可以通过.bak文件恢复到修改之前的文件
            # 重命后，不会删除备份文件，最坏的结果是丢失当前的写入，但也会保留一份之前的备份
            os.rename(src=tmp_path,dst=file_path)
        

def pkl_load(file_path, use_joblib=False):
    """ 
    与pkl_load配对使用
    """
    if use_joblib:
        data = joblib.load(file_path)
        return data

    try:
        with open(file_path, 'rb') as f:
            data_dict = pkl.load(f)
        data = tuple(list(data_dict.values()))
        if len(data) == 1:
            return data[0]
        return data 
    except Exception as e:
    #     print(repr(e))
        model = joblib.load(file_path)
        return model 


def str_pd(data,cname_date_type):
    """pandas数表列转字符类型"""
    data[cname_date_type] = data[cname_date_type].astype(str)
    data[cname_date_type] = data[cname_date_type].astype("string")
    return data


def null_deal_pandas(data,cname_num_type=[], cname_str_type=[], num_padding=0, str_padding = '<PAD>'):
    """
    params
    ----------------------------------
    - data:pandas数表
    - cname_num_type：数字类型列表
    - cname_str_type：字符类型列表
    - num_padding:数字类型空值填充
    - str_padding:字符类型空值填充
    
    example
    -----------------------------------
    #空值处理
    data = null_deal_pandas(data,cname_num_type=num_type,cname_str_type=str_classification,num_padding=0,str_padding = '<PAD>')

    """
    if len(cname_num_type)>0:
        # 数字置为0
        for col in cname_num_type:
            data.loc[data[col].isna(),col]=num_padding
    
    if len(cname_str_type)>0:
        #object转str，仅处理分类特征，身份认证类特征不参与训练
        data[cname_str_type] = data[cname_str_type].astype(str)
        data[cname_str_type] = data[cname_str_type].astype("string")
        
        for col in cname_str_type:
            data.loc[data[col].isna(),col]=str_padding

        # nan被转为了字符串，但在pandas中仍然是个特殊存在，转为特定字符串，以防Pandas自动处理
        # 创建一个替换映射字典  
        type_mapping = {  
            'nan': str_padding,   
            '': str_padding
        }  
            
        # 使用.replace()方法替换'列的类型'列中的值  
        data[cname_str_type] = data[cname_str_type].replace(type_mapping)  
            
        nu = data[cname_str_type].isnull().sum()
        for col_name,v in nu.items():
            if v > 0 :
                print("存在空值的列:\n")
                print(col_name,v)
        return data

def min_max_scaler(df):  
    return (df - df.min()) / (df.max() - df.min())  

def std7(df, cname_num, means=None, stds=None, set_7mean=True):
    if set_7mean: #将超过7倍均值的数据置为7倍均值
        # 遍历DataFrame的每一列,
        for col in cname_num:  
            # 获取当前列的均值  
            mean_val = means[col]  
            # 创建一个布尔索引，用于标记哪些值超过了均值的7倍  
            mask = df[col] > (7 * mean_val)  
            # 将这些值重置为均值的7倍  
            df.loc[mask, col] = 7 * mean_val  

    df[cname_num] = (df[cname_num] - means)/stds  #标准化
    
    return df  

def get_logical_types(col_type):
    """featuretools逻辑类型处理
    - 主要处理日期与字符串两类，即将日期，字符串类型的字段转换为featuretools的类型
    - 数字不需要处理，因为featuretools会默认把数字形式的字符串当数字处理
    """
    logical_types={}
    for col in col_type.date_type:
        logical_types[col] = 'datetime'
    
    #类别本来不是数字，但onehot编码后，就只剩下0与1这两个数字了
    for col in col_type.str_classification:
        logical_types[col] = 'categorical'

    return logical_types


class ColumnType:
    def __init__(self):
        self.num_type = []          # 数字类
        self.bool_type = []          # 整数类
        self.date_type = []         # 日期类
        self.str_identity= []       # 标识
        self.str_classification=[]  # 类别
        self.feature_names = []     # 特征组合列
        self.feature_names_num= []  # 特征组合列之数字特征
        self.feature_names_str=[]   # 特征组合列之类别特征
        self.feature_logical_types={}


def data_classify_deal(data, col_type, pc,dealnull=False,dealstd=False,deallowdata=False,lowdata=10,deallog=False):
    """数据分类处理
    - 日期处理
    - object转string
    - 空值处理
    - 数字处理
        - 边界：极小-舍弃10￥以下交易，极大-重置超过7倍均值的金额
        - 分布：Log10后标准化
        - 最终的数据值不大，并且是以0为中心的正态分布

    - 处理后的数据类型：数字，日期，字符
    -
    
    params
    --------------------------------
    - dealnull:是否同时处理空值
    - dealstd:是否进行标准化处理
    - deallog:是否对数字列log10处理
    
    example
    ----------------------------------
    data_classify_deal(data,pc.col_type_nolable,pc)
    
    """
    column_all = data.columns
     
     
    ### 日期
    date_type = [col for col in col_type.date_type if col in column_all] 
    data = str_pd(data, date_type)
    for col in date_type:
        data[col] = pd.to_datetime(data[col], errors='coerce')  

    ### 数字
    num_type = [col for col in col_type.num_type if col in column_all] 
    data[num_type] = data[num_type].astype(np.float32)
    
    
    bool_type = [col for col in col_type.bool_type if col in column_all]
    data[bool_type] = (data[bool_type].astype(np.float32)).astype(int)  # 为了处理'0.00000000'

    ### 字符-身份标识类
    cname_str_identity = pc.cname_str_identity 
    str_identity = [col for col in column_all if col in cname_str_identity]
    col_type.str_identity = str_identity
    data = str_pd(data,str_identity)

    ### 字符-分类，用于分类的列，比如渠道，交易类型,商户，地区等
    str_classification = [col for col in data.columns if col not in str_identity and col not in num_type and col not in date_type and col not in bool_type]
    col_type.str_classification = str_classification
    data = str_pd(data,str_classification)

    #空值处理
    if dealnull:
        data = null_deal_pandas(data,cname_num_type=num_type,cname_str_type=str_classification,num_padding=0,str_padding = '<PAD>')

    if len(num_type)>0:
        if deallowdata:
            #数字特征-极小值处理
            #将小于10￥的金额全部置为0，即不考虑10￥以下的交易
            for col_name in num_type:
                data.loc[data[col_name]<lowdata,col_name] = lowdata
        
            #将lowdata以下交易剔除
            data.drop(data[data.CNY_AMT.eq(10)].index, inplace=True)
        if deallog:
            #防止后面特征组合时，两个本来就很大的数据相乘后变为inf
            data[num_type] = np.log10(data[num_type])
    
        if dealstd:
            # 数字特征-归一化及极大值处理
            #需要保存，预测时使用
            means = data[num_type].mean()
            stds = data[num_type].std()
            
            data = std7(data, num_type, means, stds)
    

    return data
    
    
from sklearn import tree
from sklearn.tree import _tree


def Get_Rules(clf,X):
    n_nodes = clf.tree_.node_count
    children_left = clf.tree_.children_left
    children_right = clf.tree_.children_right
    feature = clf.tree_.feature
    threshold = clf.tree_.threshold
    value = clf.tree_.value
    
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves  = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, 0)]
    
    while len(stack) > 0:
        
        node_id, depth = stack.pop()
        node_depth[node_id] = depth
    
        is_split_node = children_left[node_id] != children_right[node_id]
        
        if is_split_node:
            stack.append((children_left[node_id],  depth+1))
            stack.append((children_right[node_id], depth+1))
        else:
            is_leaves[node_id] = True  
    feature_name = [
            X.columns[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in clf.tree_.feature]
    
    ways  = []
    depth = []
    feat = []
    nodes = []
    rules = []
    for i in range(n_nodes):   
        if  is_leaves[i]: 
            while depth[-1] >= node_depth[i]:
                depth.pop()
                ways.pop()    
                feat.pop()
                nodes.pop()
            if children_left[i-1]==i:#当前节点是上一个节点的左节点，则是小于
                a='{f}<={th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))
                ways[-1]=a              
                last =' & '.join(ways)+':'+str(value[i][0][0])+':'+str(value[i][0][1])
                rules.append(last)
            else:
                a='{f}>{th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))
                ways[-1]=a
                last = ' & '.join(ways)+':'+str(value[i][0][0])+':'+str(value[i][0][1])
                rules.append(last)
               
        else: #不是叶子节点 入栈
            if i==0:
                ways.append(round(threshold[i],4))
                depth.append(node_depth[i])
                feat.append(feature_name[i])
                nodes.append(i)             
            else: 
                while depth[-1] >= node_depth[i]:
                    depth.pop()
                    ways.pop()
                    feat.pop()
                    nodes.pop()
                if i==children_left[nodes[-1]]:
                    w='{f}<={th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))
                else:
                    w='{f}>{th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))              
                ways[-1] = w  
                ways.append(round(threshold[i],4))
                depth.append(node_depth[i]) 
                feat.append(feature_name[i])
                nodes.append(i)
    return rules

from sklearn import tree
from sklearn.tree import _tree

def rules_clf_base(clf,X):
    n_nodes = clf.tree_.node_count
    children_left = clf.tree_.children_left
    children_right = clf.tree_.children_right
    feature = clf.tree_.feature
    threshold = clf.tree_.threshold
    value = clf.tree_.value
    
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves  = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, 0)]
    
    while len(stack) > 0:
        
        node_id, depth = stack.pop()
        node_depth[node_id] = depth
    
        is_split_node = children_left[node_id] != children_right[node_id]
        
        if is_split_node:
            stack.append((children_left[node_id],  depth+1))
            stack.append((children_right[node_id], depth+1))
        else:
            is_leaves[node_id] = True  
    feature_name = [
            X.columns[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in clf.tree_.feature]
    
    ways  = []
    depth = []
    feat = []
    nodes = []
    rules = []
    for i in range(n_nodes):   
        if  is_leaves[i]: 
            while depth[-1] >= node_depth[i]:
                depth.pop()
                ways.pop()    
                feat.pop()
                nodes.pop()
            if children_left[i-1]==i:#当前节点是上一个节点的左节点，则是小于
                a='{f}<={th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))
                ways[-1]=a              
                last =' & '.join(ways)+':'+str(value[i][0][0])+':'+str(value[i][0][1])
                rules.append(last)
            else:
                a='{f}>{th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))
                ways[-1]=a
                last = ' & '.join(ways)+':'+str(value[i][0][0])+':'+str(value[i][0][1])
                rules.append(last)
               
        else: #不是叶子节点 入栈
            if i==0:
                ways.append(round(threshold[i],4))
                depth.append(node_depth[i])
                feat.append(feature_name[i])
                nodes.append(i)             
            else: 
                while depth[-1] >= node_depth[i]:
                    depth.pop()
                    ways.pop()
                    feat.pop()
                    nodes.pop()
                if i==children_left[nodes[-1]]:
                    w='{f}<={th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))
                else:
                    w='{f}>{th}'.format(f=feat[-1],th=round(threshold[nodes[-1]],4))              
                ways[-1] = w  
                ways.append(round(threshold[i],4))
                depth.append(node_depth[i]) 
                feat.append(feature_name[i])
                nodes.append(i)
    return rules

# 判断对象是否为 DataFrame 类型  

def is_dataframe(obj):  
    return isinstance(obj, pd.DataFrame) 

def rules_clf2(X,y,columns=None,max_depth=5,top_n=None,):
    """二分类问题规则生成
    - 按异常样本的含量排序，
    - 100%是异常样本，与0%是异常样本同样有用，它们都是纯净的数据，看实际需要提取哪个
    """
    if not is_dataframe(X):
        if columns is not None:
            X=pd.DataFrame(X,columns=columns)
            y=pd.DataFrame(y,columns=['label'])
        else:
            return 'X与y非pandas数表时，请指定 columns'

    #训练一个决策树，这里限制了最大深度和最小样本树
    clf = tree.DecisionTreeClassifier(max_depth=max_depth,min_samples_leaf=50)
    clf = clf.fit(X, y)
    rules = rules_clf_base(clf,X)
    
    # 结果格式整理
    df = pd.DataFrame(rules)
    df.columns = ['allrules']
    df['rules']    = df['allrules'].str.split(':').str.get(0)
    df['good']     = df['allrules'].str.split(':').str.get(1).astype(float)
    df['bad']      = df['allrules'].str.split(':').str.get(2).astype(float)
    df['all']      = df['bad']+df['good']
    df['rate'] = df['bad']/df['all']
    df.drop(columns=['good','bad','all'],inplace=True)
    df = df.sort_values(by='rate',ascending=False)
    del df['allrules']
    if top_n:
        return df[:top_n]
    else:
        return df
    
    
import random

def random_str(seq_len=(1,3)):
    """随机生成seq_len[0]到 seq_len[1]长度的字符串
    - 字符串由字母与数字组成
    """
    # 单词集合，对应键盘上的字母
    words = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
        'q', 'w', 'e', 'r',  't', 'y',  'u', 'i', 'o', 'p', 
        'a', 's', 'd', 'f',  'g', 'h',  'j', 'k', 'l', 
        'z', 'x', 'c', 'v',  'b', 'n',  'm'
    ]
        
    # 每个词被选中的概率，随机初始化的概率
    p = np.array([
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
        1,   2,  3,  4,  5,  6,  7,  8,  9, 10, 
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
    ])
    
    # 转概率，所有单词的概率之和为1
    p = p / p.sum()
    
    # 随机选n个词
    # Return random integer in range [a, b], including both end points.
    n = random.randint(seq_len[0], seq_len[1])
    x = np.random.choice(words, size=n, replace=True, p=p)

def random_str_list(n=5,seq_len=(1,3)):
    """生成字符串列表
    """
    tmp = []
    for i in range(n):
        tmp.append(random_str(seq_len))
    return tmp 


def is_single_label(y_test, y_pred):
    """预测集与预测值是否同时为相同的一个值，此时无法计算AUC"""
    label_test = pd.DataFrame(y_test).value_counts()
    label_pred = np.unique(y_pred)
    if len(label_test) == len(label_pred):
        if label_test[0] ==label_pred[0]:
            return True
    return False


def model_evaluate(y_probs,y_test):
    """模型评估
    params
    -------------------------------------------------------
    - y_probs:模型概率输出,1维，每个元素为 标签1的概率，即正样本概率列表
    - y_test:真实标签，1维
    
    return
    -------------------------
    - acc,precision,recall,f1,auc ,依次为准确率，精确率，召回率，f1值，AUC 
    - 其中精确率，召回率只针对 正样本-1
    
    examples
    --------------------------------------------------------
    acc,precision,recall,f1,auc  = model_evaluate(y_probs,y_test)
    """
    if y_probs.ndim !=1:
        raise Exception(f"y_probs必须为1维，实际为{y_probs.ndim }维")
    # 定义预测结果：概率>0.5则预测结果为 1 即可疑；概率<=0.5则预测结果为0 即不可疑
    y_pred = np.where(y_probs>0.5,1,0)
    is_single_value = is_single_label(y_test, y_pred)
    if is_single_value:
        roc_auc = 1
    else:
        # auc = roc_auc_score(y_test, y_pred)
        # 计算ROC曲线和AUC值
        fpr, tpr, thresholds = roc_curve(y_test, y_probs)
        roc_auc = auc(fpr, tpr)
    
    
    conf_matrix = confusion_matrix(y_test, y_pred)
    acc = (conf_matrix[0,0]+conf_matrix[1,1])/(conf_matrix[0,0]+conf_matrix[1,0]+conf_matrix[0,1]+conf_matrix[1,1])

    #对正样本的预测精度
    pre_1 = conf_matrix[0,1]+conf_matrix[1,1]
    true_1 = conf_matrix[1,0]+conf_matrix[1,1]
    if pre_1==0 and true_1>0: #真实1个数不为0，但预测为1的个数为0，则精确率为0 
        precision = 0
    elif pre_1==0:#预测可疑样本数为0 这个很可能会出现  比如一批样本中真的就没有可疑的 模型本身预测正样本的能力也差 
        precision = 1
    else:
        precision = float(conf_matrix[1,1])/pre_1

    # Recall 召回率
    real_1_num = conf_matrix[1,0]+conf_matrix[1,1]
    if real_1_num==0: #即真实的可疑样本个数为0，即一批样本中的数据都是正常的 
        recall = 1 
    else:
        recall = float(conf_matrix[1,1])/real_1_num

    f1 = 2/(1/(precision+1e-6)+1/(recall+1e-6))

    #保留2位有效数字
    acc = np.around(acc,decimals=4)
    precision = np.around(precision,decimals=4)
    recall = np.around(recall,decimals=4)
    f1 = np.around(f1,decimals=4)
    roc_auc = np.around(roc_auc,decimals=4)

    #默认AI预测达不到1 即达不到100%准确,最多99%
    if acc>=1:
        acc = 0.9999
    if precision>=1:
        precision = 0.9999
    if recall>=1:
        recall = 0.9999
    if f1>=1:
        f1 = 0.9999
    if roc_auc>=1:
        roc_auc = 0.9999
    return acc,precision,recall,f1,roc_auc 


