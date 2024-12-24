"""
方法直接放tpf的__init__方法中
除以下两个
python基础方法，
data集获取方法 
"""

from tpf.link.datadeal import DateDeal 

from tpf.link.db import OracleDb,reset_passwd

from tpf.link.train_ml import Link 
from tpf.link.train_ml import MLib
from tpf.link.train_ml import ModelPre

from tpf.link.toolml import Corr
from tpf.link.toolml import FeatureEval 
from tpf.link.toolml import ModelEval
from tpf.link.toolml import model_evaluate
from tpf.link.toolml import rules_clf2
from tpf.link.toolml import null_deal_pandas,std7,min_max_scaler
from tpf.link.toolml import str_pd,get_logical_types,ColumnType
from tpf.link.toolml import data_classify_deal
from tpf.link.toolml import pkl_save,pkl_load
from tpf.link.toolml import random_str_list,random_str


