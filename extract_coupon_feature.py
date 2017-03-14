#!/usr/bin/python 
#-*- coding: UTF-8 -*-   

import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

def extract_coupon_feature(dataset_file_path,num):
	print '第{0}个样本提取'.format(num)
	dataset = pd.read_csv(dataset_file_path)
	coupon = dataset[['Coupon_id']]
	coupon.drop_duplicates(inplace=True)

	t1 = dataset[['Coupon_id','Discount_rate']]
	t1.drop_duplicates(inplace=True)
	t1['discount_man'] = t1.Discount_rate.apply(get_discount_man)
	t1['discount_jian'] = t1.Discount_rate.apply(get_discount_jian)
	t1['is_man_jian'] = t1.Discount_rate.apply(is_man_jian)
	t1['Discount_rate'] = t1.Discount_rate.apply(calc_discount_rate)
	
	coupon = pd.merge(coupon,t1,on='Coupon_id',how='left')

	coupon.Discount_rate = coupon.Discount_rate.replace(np.nan,0)
	coupon.to_csv('data/coupon{0}.csv'.format(num),index=None)
    

if __name__ == '__main__':
	for k,path in enumerate(processed_dataset_path):
    	extract_coupon_feature(path,k+1)