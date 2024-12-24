'''
Description: 基础功能
Author: 七三学徒
Date: 2022-01-25 15:30:42
'''
import numpy as np 
import os ,time 


def has_key(dct,key):
    res = key in list(dct.keys())
    return res 

def stp(data, msg=None):
    """print shape type
    """
    ss = "shape:{}, type:{}".format(data.shape,type(data))
    if msg:
        ss = "{}, {}".format(ss,msg)

    print(ss)



if __name__=="__main__":
    from tpf.vec3 import matrix_multiply

    a = np.arange(6).reshape(2,3)

    b = np.arange(6).reshape(3,2)

    c=matrix_multiply(a,b)
    
    print(c)


