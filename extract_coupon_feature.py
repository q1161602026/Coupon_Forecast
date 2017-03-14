#!/usr/bin/python 
#-*- coding: UTF-8 -*-   

import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

def extract_coupon_feature(feature_file_path,num):
	print '第{0}个样本提取'.format(num)
	feature = pd.read_csv(feature_file_path)
	feature = feature[feature['Coupon_id']!='null']
    
	coupon = feature[['Coupon_id']]
	coupon.drop_duplicates(inplace=True)

	t1 = feature[['Coupon_id','Discount_rate']]
	t1.drop_duplicates(inplace=True)
	t1['discount_man'] = t1.Discount_rate.apply(get_discount_man)
	t1['discount_jian'] = t1.Discount_rate.apply(get_discount_jian)
	t1['is_man_jian'] = t1.Discount_rate.apply(is_man_jian)
	t1['Discount_rate'] = t1.Discount_rate.apply(calc_discount_rate)

	t2 = feature[['Coupon_id']]
	t2['coupon_count'] = 1
	t2 = t2.groupby('Coupon_id').agg('sum').reset_index()

	coupon = pd.merge(coupon,t1,on='Coupon_id',how='left')
	coupon = pd.merge(coupon,t2,on='Coupon_id',how='left')

	coupon.Discount_rate = coupon.Discount_rate.replace(np.nan,0)
    
	coupon.drop_duplicates(inplace=True)
	coupon.to_csv('data/coupon{0}.csv'.format(num),index=None)
if __name__ == '__main__':
	for k,path in enumerate(processed_feature_path):
    	extract_coupon_feature(path,k+1)